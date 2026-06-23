import json
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import requests

from .paths import EPISODE_LIST_PATH, TORRENT_DIR

NYAA_BASE_URL = "https://nyaa.si/"
DEFAULT_RESOLUTIONS = ("1080", "720", "480")
REQUEST_HEADERS = {
	"User-Agent": "Mozilla/5.0 (compatible; anidown/1.0)"
}


def obtainjson(url):
	try:
		return requests.get(url, headers=REQUEST_HEADERS, timeout=30)
	except Exception:
		time.sleep(5)
		return obtainjson(url)


def loadlist():
	with EPISODE_LIST_PATH.open("r", encoding="utf-8") as read_file:
		return json.load(read_file)


def savelist(edited):
	EPISODE_LIST_PATH.parent.mkdir(parents=True, exist_ok=True)
	with EPISODE_LIST_PATH.open("w", encoding="utf-8") as outfile:
		json.dump(edited, outfile, indent=4)


def animeinfo(currentanime):
	return currentanime[0], currentanime[1][0], currentanime[1][1]


def build_rss_url(query, category="1_2", filter_value="0"):
	return "{}?{}".format(NYAA_BASE_URL, urlencode({
		"page": "rss",
		"q": query,
		"c": category,
		"f": filter_value,
	}))


def normalize_episode(nextepi):
	return "{:02d}".format(nextepi) if nextepi < 10 else str(nextepi)


def safe_filename(name):
	return re.sub(r'[<>:"/\\|?*]', "_", name).strip()


def rss_items(rss_text):
	root = ET.fromstring(rss_text)
	for item in root.findall("./channel/item"):
		title = item.findtext("title", default="")
		link = item.findtext("link", default="")
		yield title, link


def title_matches(title, subber, episode, resolution):
	return (
		subber.lower() in title.lower()
		and re.search(r"(^|[^0-9]){}([^0-9]|$)".format(re.escape(episode)), title)
		and "({}p)".format(resolution) in title
	)


def download_torrent(title, link, destination_dir=None):
	if not link:
		return None
	response = requests.get(link, headers=REQUEST_HEADERS, allow_redirects=True, timeout=30)
	response.raise_for_status()
	content_type = response.headers.get("Content-Type", "")
	if "bittorrent" not in content_type and not response.content.startswith(b"d"):
		raise ValueError("Unexpected torrent response from {}".format(link))
	target_dir = Path(destination_dir) if destination_dir else TORRENT_DIR
	target_dir.mkdir(parents=True, exist_ok=True)
	filename = target_dir / (safe_filename(title) + ".torrent")
	filename.write_bytes(response.content)
	print(title)
	print(link)
	print(filename)
	print("\n")
	return filename


def processpage(url, i, subber, nextepi, resolution, animename, destination_dir=None):
	current_time = datetime.now().strftime("%H:%M:%S")
	print("[{}] Processing - {} Episode {}\n=====================".format(current_time, animename, nextepi))
	query = "{} {} {}".format(subber, animename, resolution)
	rss_url = build_rss_url(query)
	word = obtainjson(rss_url).text
	return getrows(word, subber, nextepi, resolution, destination_dir)


def getrows(rss_text, subber, nextepi, resolution, destination_dir=None):
	nextepi = normalize_episode(nextepi)
	for temp_title, temp_download in rss_items(rss_text):
		if title_matches(temp_title, subber, nextepi, resolution):
			try:
				return download_torrent(temp_title, temp_download, destination_dir)
			except Exception as error:
				print("Error downloading torrent: {}".format(error))
				return None
	print("\n")
	return None


def processpage_with_resolution_fallback(subber, nextepi, animename, resolutions=DEFAULT_RESOLUTIONS, destination_dir=None):
	for resolution in resolutions:
		download_path = processpage(None, None, subber, nextepi, resolution, animename, destination_dir)
		if download_path:
			return resolution, download_path
	return None, None
