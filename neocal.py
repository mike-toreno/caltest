#!/usr/bin/python3.5

import requests
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

current_time = datetime.datetime.utcnow()
current_time = datetime.datetime.strftime(current_time, '%Y-%m-%dT%H:%M:%S+00:00')
j = 0
found_events = []

for i in range(len(cal.events)): 
	if timeconv(str(cal.events[i].end)) == timeconv(str(current_time)):
		found_events.append(str(cal.events[i].name))
		j += 1

for i in range(len(found_events)):
	print(str(i + 1) + ". " + found_events[i])
