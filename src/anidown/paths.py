from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]
DATA_DIR = PROJECT_ROOT / "data"
EPISODE_LIST_PATH = DATA_DIR / "latest_episodetest.json"
TORRENT_DIR = PROJECT_ROOT / "downloads" / "torrents"
