# mal_scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

class MALScraper:
    BASE_URL = "https://myanimelist.net/anime"

    def __init__(self, delay=2.0):
        """
        delay: seconds to wait between requests to avoid rate-limiting
        """
        self.delay = delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MALScraper/1.0; +https://github.com/)"
        }

    def get_episode_count_by_url(self, url):
        """Scrape a MyAnimeList anime page by its URL"""
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch {url}: Status {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        episodes_label = soup.find("span", text="Episodes:")
        if episodes_label and episodes_label.next_sibling:
            ep_text = episodes_label.next_sibling.strip()
            try:
                return int(ep_text)
            except ValueError:
                # Handle cases like "Unknown" or "?"
                return None
        return None

    def get_episode_count_by_search(self, title):
        """
        Search MAL for a title, take the first result, and return its episode count.
        """
        search_url = f"https://myanimelist.net/anime.php?q={quote(title)}"
        response = requests.get(search_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch search results: Status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        # Grab first search result link
        first_result = soup.select_one("a.hoverinfo_trigger")
        if not first_result:
            raise Exception("No results found on MAL for your query")

        anime_url = first_result['href']
        return self.get_episode_count_by_url(anime_url)
