from mal import Anime, AnimeSearch
import requests
import json
import html_to_json
from prettyprinter import pprint
import processor as pros
import time
while True:
	searchword = 'horimiya'
	subber = '[SubsPlease]'
	downloadprefix = 'https://nyaa.si'
	url = 'https://nyaa.si/?f=0&c=1_2&q='+subber+' '+searchword
	resolution = '720'
	with open("latest_episodes.json", "r") as read_file:
	    currentepisode = json.load(read_file)
	read_file.close()
	animelist = list(currentepisode.keys())
	# print(animelist)
	nextepi = currentepisode[searchword]+1
	print('{0} watched until episode: {1}'.format(searchword,currentepisode[searchword]))
	# search = AnimeSearch(searchword) # Search for "cowboy bebop"
	# topresult = search.results[0]

	# print(topresult.mal_id) # Get title of first result

	# anime = Anime(42897)
	# print(anime.title)
	# print(anime.broadcast)
	word = pros.obtainjson(url).text
	output_json = html_to_json.convert(word)
	anime_title = output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'][0]['td'][1]['a'][0]['_attributes']['title']
	anime_download = downloadprefix+output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'][0]['td'][2]['a'][0]['_attributes']['href']
	anime_rows = len(output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'])
	# print(anime_title)
	# print(anime_download)
	# pprint(output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'][0]['td'][1]['a'][1]['_attributes']['title'])
	# print(anime_rows)

	for i in range(anime_rows):
		anime_selection = output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'][i]
		temp_title = anime_selection['td'][1]['a'][0]['_attributes']['title']
		if(temp_title.find('comments')!=-1 or temp_title.find('comment')!=-1):
			temp_title = anime_selection['td'][1]['a'][1]['_attributes']['title']
		if(temp_title.find(subber)!=-1 and temp_title.find(str(nextepi)+' ')!=-1 and temp_title.find(resolution)!=-1):
			temp_download = downloadprefix+anime_selection['td'][2]['a'][0]['_attributes']['href']
			print(temp_title)
			print(temp_download)
			r = requests.get(temp_download, allow_redirects=True)
			open(temp_title+'.torrent', 'wb').write(r.content)
			currentepisode[searchword] = nextepi
			edited = json.dumps(currentepisode)
			with open("latest_episodes.json", "w") as outfile:
				outfile.write(edited)
	print('Current episode after search: ',currentepisode[searchword])
	time.sleep(60)
