import time

from . import processor as pros
from .mal_scraper import MALScraper


def run(interval_seconds=60):
	scraper = MALScraper()

	while True:
		epidump = pros.loadlist()
		epilist = list(epidump.items())
		for currentanime in epilist:
			animename, animesubber, animeepisode = pros.animeinfo(currentanime)
			episodes = scraper.get_episode_count_by_search(animename)
			print(f"Total episodes for {animename}: {episodes}")
			if animeepisode == episodes:
				break

			animeepisode_next = animeepisode + 1
			resolution, download_path = pros.processpage_with_resolution_fallback(animesubber, animeepisode_next, animename)
			if resolution is not None:
				print("Downloaded {}p".format(resolution))
				print(download_path)
				epidump[animename][1] = animeepisode_next
		pros.savelist(epidump)
		time.sleep(interval_seconds)
