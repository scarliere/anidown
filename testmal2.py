import json
from prettyprinter import pprint
import processor as pros
import time
while True:
	epidump = pros.loadlist()
	epilist = list(epidump.items())
	# print(epilist)
	for i in range(len(epilist)):
		currentanime = epilist[i]
		animename, animesubber, animeepisode = pros.animeinfo(currentanime)
		# print(animename,animesubber,animeepisode)
		resolution = '720'
		url = 'https://nyaa.si/?f=0&c=1_2&q={0} {1} {2}'.format(animesubber,animename,resolution)
		animeepisode_next = animeepisode+1
		# print(url)
		if(pros.processpage(url,i,animesubber,animeepisode_next,resolution,animename)==True):
			epidump[animename][1]=animeepisode_next
	pros.savelist(epidump)
	
	
	

	# for i in range(anime_rows):
	# 	anime_selection = output_json['html'][0]['body'][0]['div'][0]['div'][0]['table'][0]['tbody'][0]['tr'][i]
	# 	temp_title = anime_selection['td'][1]['a'][0]['_attributes']['title']
	# 	if(temp_title.find('comments')!=-1 or temp_title.find('comment')!=-1):
	# 		temp_title = anime_selection['td'][1]['a'][1]['_attributes']['title']
	# 	if(temp_title.find(subber)!=-1 and temp_title.find(str(nextepi)+' ')!=-1 and temp_title.find(resolution)!=-1):
	# 		temp_download = downloadprefix+anime_selection['td'][2]['a'][0]['_attributes']['href']
	# 		print(temp_title)
	# 		print(temp_download)
	# 		r = requests.get(temp_download, allow_redirects=True)
	# 		open(temp_title+'.torrent', 'wb').write(r.content)
	# 		currentepisode[searchword] = nextepi
	# 		edited = json.dumps(currentepisode)
	# 		with open("latest_episodes.json", "w") as outfile:
	# 			outfile.write(edited)
	# print('Current episode after search: ',currentepisode[searchword])
	break

