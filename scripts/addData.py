import csv
import os
import psycopg2
import json

collision_files = ['../data/cleaned/accident-dim/collisionsOttawa2013.csv']
 				# 	'../data/cleaned/accident-dim/collisionsOttawa2014.csv',
 				# 	"../data/cleaned/accident-dim/collisionsOttawa2015.csv",
 				# 	"../data/cleaned/accident-dim/collisionsOttawa2016.csv",
					# "../data/cleaned/accident-dim/collisionsOttawa2017.csv"] 

weather_files = ['../data/cleaned/hour/hourly2018.csv']

def add_collision_data():
	with open("creds.json", 'r') as f:
		creds = json.load(f)
	conn = None
	try:
		conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
		cursor = conn.cursor()
		for file in collision_files:
			with open(file) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				rowNum = 0
				for row in csv_reader:
					if rowNum != 0:
						collision_INSERT = """INSERT INTO accident(accident_key,accident_time,environment,road_surface,traffic_control,visibility,impact_type) """\
						"""VALUES (%s, %s, %s, %s, %s, %s, %s)"""
						cursor.execute(collision_INSERT,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],))
					rowNum = rowNum+1
		cursor.close()
		conn.commit()
		print("THE ENDDDDDD!!!!!!")
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def add_hour_data():
	with open("creds.json", 'r') as f:
		creds = json.load(f)
	conn = None
	try:
		conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
		cursor = conn.cursor()
		for file in weather_files:
			with open(file) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				rowNum = 0
				for row in csv_reader:
					if rowNum != 0:
						hour_INSERT = """INSERT INTO hour(hour_key,hour_start,hour_end,currDate,day_of_week,month,year, weekend, holiday, holiday_name) """\
						"""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
						cursor.execute(hour_INSERT,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],))
					rowNum = rowNum+1
		cursor.close()
		conn.commit()
		print("THE ENDDDDDD!!!!!!")
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


def add_location_data():
	with open("creds.json", 'r') as f:
		creds = json.load(f)
	conn = None
	try:
		conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
		cursor = conn.cursor()
		for file in collision_files:
			with open(file) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				rowNum = 0
				for row in csv_reader:
					if rowNum != 0:
						location_INSERT = """INSERT INTO location(location_key,streetName_highway,intersection1_offramp1,intersection2_offramp2,longitude,latitude,neighborhood) """\
						"""VALUES (%s, %s, %s, %s, %s, %s, %s)"""
						cursor.execute(location_INSERT,(row[7],row[13],row[14],row[15],row[8],row[9],row[16],))
					rowNum = rowNum+1
		cursor.close()
		conn.commit()
		print("THE ENDDDDDD!!!!!!")
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

add_location_data()
					
def add_weather_data():
	with open("creds.json", 'r') as f:
		creds = json.load(f)
	conn = None
	try:
		conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
		cursor = conn.cursor()
		for file in collision_files:
			with open(file) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				for row in csv_reader:
					print(row[0])
					weather_INSERT = """INSERT INTO weather(weather_key, station_name, longitude, latitude, temperature, visibility, wind_speed, wind_chill, wind_direction, pressure) """\
					"""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
					cursor.execute(weather_INSERT,(row[0],row[7],row[8],row[10],row[11],row[12],row[14],))
		cursor.close()
		conn.commit()
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def add_location_data():
	with open("creds.json", 'r') as f:
		creds = json.load(f)
	conn = None
	try:
		conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
		cursor = conn.cursor()
		for file in collision_files:
			with open(file) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				rowNum = 0
				for row in csv_reader:
					if rowNum != 0:
						location_INSERT = """INSERT INTO location(location_key,streetName_highway,intersection1_offramp1,intersection2_offramp2,longitude,latitude,neighborhood) """\
						"""VALUES (%s, %s, %s, %s, %s, %s, %s)"""
						cursor.execute(location_INSERT,(row[7],row[14],row[15],row[16],row[9],row[10],row[6],))
					rowNum = rowNum+1
		cursor.close()
		conn.commit()
		print("THE ENDDDDDD!!!!!!")
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


