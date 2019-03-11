import datetime
from dateutil import rrule
from datetime import timedelta
import csv
import argparse
import sys
import os
import collections
import holidays
from datetime import date

STARTDATE = datetime.datetime(2013, 1, 1)
ENDDATE = datetime.datetime(2019, 1, 1)
hundredDaysLater = STARTDATE + timedelta(days=100)
CLEAN_DIR = "../data/cleaned/hour"
holidays = holidays.Canada()

def allHours():
	field_names = ["HOUR_KEY", "HOUR_START", "HOUR_END", "DATE", "DAY_OF_WEEK", "MONTH", "YEAR", "WEEKEND","HOLIDAY", "HOLIDAY_NAME"]
	hour_iterID = 0
	for dy in rrule.rrule(rrule.YEARLY, dtstart=STARTDATE, until=ENDDATE):
		year = dy.year
		filename = "hourly"+str(dy.year)+".csv"
		writer = csv.DictWriter(open(f"{CLEAN_DIR}/{filename}",'w'), fieldnames=field_names)
		writer.writeheader()
		for dt in rrule.rrule(rrule.HOURLY, dtstart=datetime.datetime(year, 1, 1), until=datetime.datetime(year,12,31,23,59,59)):

			new_row={}
			new_row["HOUR_KEY"]=hour_iterID
			hour_iterID=hour_iterID+1
			new_row["HOUR_START"]=dt.strftime("%X")
			p1hour=(dt+timedelta(hours=1)-timedelta(seconds=1)).strftime("%X")
			new_row["HOUR_END"]=p1hour
			new_row["DATE"]=dt.strftime("%Y-%m-%d")
			new_row["DAY_OF_WEEK"]=dt.strftime("%A")
			new_row["MONTH"]=dt.strftime("%B")
			new_row["YEAR"]=dt.year
			if dt.strftime("%w") == 0 or dt.strftime("%w") == 6:
				new_row["WEEKEND"]=True
			else:
				new_row["WEEKEND"]=False
			if dt in holidays:
				new_row["HOLIDAY"]=True
				new_row["HOLIDAY_NAME"]=holidays[dt]
			else:
				new_row["HOLIDAY"]=False
				new_row["HOLIDAY_NAME"]=''
			writer.writerow(new_row)

allHours()
