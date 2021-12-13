#!/usr/bin/env python3

import sys
import requests
from flask_table import Table, Col

base_url = 'https://api.brawlstars.com/v1/players/%23'
event_url = 'https://api.brawlstars.com/v1/events/rotation'
API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjJmMDVmMjgyLTRlYTAtNGVjYS05NTM2LTVmNzk5MzdiMTg4NCIsImlhdCI6MTYzOTM1NDIyMSwic3ViIjoiZGV2ZWxvcGVyLzk3ZTcxNDQ1LWRmMTUtYzcyZi1iNjQ5LTc5MDNmZTNiZGJjZCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNjkuMTEyLjE5My45MyIsIjczLjE2NC4xOS4yNDkiXSwidHlwZSI6ImNsaWVudCJ9XX0.IkmBGgy5XCgi--Yuo85ttQ6TdJSubJpirwv3z_LVORNURNwUT5XkL_w4OoTiSKMVEKAO4pSeZrq6vVl4WRLB6A'
method = 'GET'
headers = {'Accept': 'application/json', 'authorization': 'Bearer ' + API_TOKEN}

RESET_FACTOR = 25

class BrawlerTable(Table):
    name = Col('Name')
    number_of_trophies = Col('Number of Trophies Lost')

# Get some objects
class BrawlerItem(object):
    def __init__(self, name, number_of_trophies):
        self.name = name
        self.number_of_trophies = number_of_trophies

def calculate_lost_trophies(brawlers):
	total_lost = 0
	items = [] 
	for brawler in brawlers:
		name = brawler['name']
		trophies = brawler['trophies']
		if trophies > 500:
			curr_loss = trophies % RESET_FACTOR
			if trophies - curr_loss > 500: # add another because they lose +1 above modding with 25
				curr_loss += 1
			items.append(BrawlerItem(name, curr_loss))
			total_lost += curr_loss
	total_message = f'You will lose {total_lost} trophies total during the trophy reset.\n'
	return (BrawlerTable(items), total_message) 

def process_request(player_id):
	if player_id:
		request_url = base_url + player_id 
		content = requests.request(method, request_url, headers=headers)
		status_code = content.status_code
		content = content.json()
		if status_code == 200:
			return (calculate_lost_trophies(content['brawlers']), 200)
		else:
			reason = content['reason']
			message = content['message']
			return (f'{reason}: {message}', status_code)
	# else:
		# content = requests.request(method, event_url, headers=headers).json()
		# events = {}
		# maps = []
		# for entry in content:
			# maps.append(entry['event']['map'])
