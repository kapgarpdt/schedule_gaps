#!/usr/bin/env python
import json
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

csvfile = "schedule_gaps.csv"
since = '2019-10-20T00:00:00-00:00'
until = '2019-11-20T00:00:00-00:00'
with open(csvfile, "a") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow( ['time_frame','schedule_name', 'rendered_coverage_percentage_final'])
	writer.writerow( [since + ' - ' + until])
	

#API_ACCESS_KEY='Msz4iBvMUp4FMRCm_Mr5'
API_ACCESS_KEY='jv7CXR3xTmyJ5i2rAMXy'
BASE_URL = 'https://api.pagerduty.com'
HEADERS = {
		'Accept': 'application/vnd.pagerduty+json;version=2',
		'Authorization': 'Token token={token}'.format(token=API_ACCESS_KEY),
		'Content-type': 'application/json'
	}

schedule_count = 0

def get_schedule_count():
	global schedule_count
	count = requests.get(BASE_URL + '/schedules', headers=HEADERS, params='total=true')
	schedule_count = count.json()['total']
	print(str(schedule_count))
	

def write_csv(row):
	with open(csvfile, 'a') as output:
		writer = csv.writer(output, lineterminator='\n')
		#print(row)
		writer.writerow(row)
		
def get_schedules(offset):
	global schedule_count
	params = {
		'offset':offset
	}
	all_schedules = requests.get(BASE_URL + '/schedules', headers=HEADERS, params=params)
	for schedule in all_schedules.json()['schedules']:
		#print(schedule['name'])
		params = {
		'since': since,
		'until':until
		}
		schedule_details = requests.get(BASE_URL + '/schedules/' + schedule['id'], headers=HEADERS, params=params)
		#printschedule_details.json())
		with open(csvfile, 'a') as output:
			writer = csv.writer(output, lineterminator='\n')
			row = ['', schedule_details.json()['schedule']['name'], schedule_details.json()['schedule']['final_schedule']['rendered_coverage_percentage']]
			#print(row)
			writer.writerow(row)
		
	    	
def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	get_schedule_count()
	for offset in xrange(0,schedule_count):
		if offset % 25 == 0:
			get_schedules(offset)
	

if __name__=='__main__':
	sys.exit(main())
