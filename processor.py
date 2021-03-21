import requests
import time
def obtainjson(url):
		try:
			return requests.get(url)
		except Exception:
			time.sleep(5)
			return obtainjson(url)