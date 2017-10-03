#!/usr/bin/python3.5 
import requests
import json
import re
from requests_oauthlib import OAuth1
import datetime
from dateutil import tz
from ics import Calendar

def timeconv(utcstring):
	utc_time = datetime.datetime.strptime(utcstring, '%Y-%m-%dT%H:%M:%S+00:00')
	utc_time = utc_time.replace(tzinfo=tz.tzutc())
	localtime = utc_time.astimezone(tz.tzlocal())
	localtime = datetime.datetime.strftime(localtime, '%Y-%m-%d')
	return localtime


cal = Calendar(requests.get('https://tockify.com/api/feeds/ics/odowdevent').text)
dayname = ""

Community = 0
MP = 0
Early = 0

Days = [[0 for i in range(4)]for j in range(3)]
#Equivalent to `int days[3][4];`
current_time = datetime.datetime.utcnow()
current_time = datetime.datetime.strftime(current_time, '%Y-%m-%dT%H:%M:%S+00:00')
j = 0
found_events = []

for i in range(len(cal.events)): 
	if timeconv(str(cal.events[i].end)) == timeconv(str(current_time)):
		found_events.append(str(cal.events[i].name))
		j += 1

for i in range(len(found_events)):
	m = re.search(r'(.*Black|.*Gold) (.*MP)', found_events[i])
	if m:
		dayname = m.group(1)
		MP = bool(m.group(2))
		break
	else:
		dayname = 'No School'
print(dayname)

if re.match('Early Dismissal', dayname):
	Early = 1
elif re.match('.*MP', dayname):
	MP = 1
elif re.match('.*Community.*', dayname):
	Community = 1

auth = OAuth1('consumer_key', 'consumer_secret', '', '')

user_name = 'User Name'
url = 'https://api.schoology.com/v1/search?keywords=' + user_name + '&type=user'
user_id = json.loads(requests.get(url, auth=auth).text)
user_id = user_id['users']['search_result'][0]['uid']
course = [None] * 12
#TODO: Allow the user to choose between search results


url = 'https://api.schoology.com/v1/users/' + user_id + '/sections'
courses_json = json.loads(requests.get(url, auth=auth).text)

for i in range(len(courses_json['section'])):
	if re.match('[0-9]{1,2}',courses_json['section'][i]['section_title']):
		course[int(re.match('[0-9]{1,2}',courses_json['section'][i]['section_title']).group(0))] = courses_json['section'][i]['course_title']

if dayname == 'No School':
	print("Placeholder")
	#Only print the calendar
elif dayname == 'Gold':
	for i in range(6, 12):
		if course[i] != None:
			print(course[i])
elif dayname == 'Black':
	for i in range(1, 6):
		if course[i] != None:
			print(course[i])
		if i == 5 and MP:
			print("MP")

"""
Java librarys:
Scribejava
KOAuth

Obejctive C:
OAuthConsumer

Swift:
OAuthSwift
"""

"""
Day Names:
Gold > 6, 7/8, 9/10, 11
Gold 5,6,7,8 MP 
Black > 1, 2, 3, 4/5
Black 1,2,3,4 MP
Early Dismissal Gold
Early Dismissal Black
Black 1,2,3/Community,4
Gold 5,6,7/Community,8
"""
"""
NOTE: This program is delibrately un-pythonic in order to make it easier to convert to other languages
"""
