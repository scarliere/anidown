import requests
import time
import json
import processor as pros
import html_to_json
from prettyprinter import pprint
from datetime import datetime

def obtainjson(url):
		try:
			return requests.get(url)
		except Exception:
			time.sleep(5)
			return obtainjson(url)
def loadlist():
	with open("latest_episodetest.json", "r") as read_file:
	    epidump = json.load(read_file)
	read_file.close()
	return epidump
def savelist(edited):
	with open("latest_episodetest.json", "w") as outfile:
		json.dump(edited, outfile,indent=4)
	outfile.close()
def animeinfo(currentanime):
	return currentanime[0], currentanime[1][0], currentanime[1][1]
def processpage(url,i,subber,nextepi,resolution,animename):
	current_time = datetime.now().strftime("%H:%M:%S")
	print('[{}] Processing - {} Episode {}\n====================='.format(current_time,animename,nextepi))
	downloadprefix = 'https://nyaa.si'
	word = pros.obtainjson(url).text
	output_json = html_to_json.convert(word)
	return getrows(output_json,subber,nextepi,resolution,downloadprefix)
def getrows(output_json,subber,nextepi,resolution,downloadprefix):
	try:
		if(nextepi<10):
			nextepi = '0'+str(nextepi)
		else: nextepi = str(nextepi)
		anime_rows = len(output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'])
		for i in range(anime_rows):
			anime_selection = output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'][i]
			temp_title = anime_selection['td'][1]['a'][0]['_attributes']['title']
			if(temp_title.find('comments')!=-1 or temp_title.find('comment')!=-1):
				temp_title = anime_selection['td'][1]['a'][1]['_attributes']['title']
			if(temp_title.find(subber)!=-1 and temp_title.find(nextepi+' ')!=-1 and temp_title.find(resolution)!=-1):
				temp_download = downloadprefix+anime_selection['td'][2]['a'][0]['_attributes']['href']
				print(temp_title)
				print(temp_download)
				r = requests.get(temp_download, allow_redirects=True)
				open(temp_title+'.torrent', 'wb').write(r.content)
				print('\n')
				return True
		print('\n')
		return False
	except Exception:
		time.sleep(5)
		print('Error')
		return getrows(output_json,subber,nextepi,resolution,downloadprefix)