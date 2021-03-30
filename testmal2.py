import json
from prettyprinter import pprint
import processor as pros
import time
while True:
	epidump = pros.loadlist()
	epilist = list(epidump.items())
	for i in range(len(epilist)):
		currentanime = epilist[i]
		animename, animesubber, animeepisode = pros.animeinfo(currentanime)
		resolution = '720'
		url = 'https://nyaa.si/?f=0&c=1_2&q={0} {1} {2}'.format(animesubber,animename,resolution)
		animeepisode_next = animeepisode+1
		if(pros.processpage(url,i,animesubber,animeepisode_next,resolution,animename)==True):
			epidump[animename][1]=animeepisode_next
	pros.savelist(epidump)
	time.sleep(60)

