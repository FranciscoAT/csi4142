import psycopg2
import json
#from config import config

CREATETABLES = [
	"""
	CREATE TABLE hour (
		hour_key INT PRIMARY KEY,
		hour_start TIME,
		hour_end TIME,
		currDate DATE,
		day_of_week VARCHAR,
		month VARCHAR,
		year INT,
		weekend VARCHAR,
		holiday VARCHAR,
		holiday_name VARCHAR
		)
	 """,
	"""
	CREATE TABLE accident (
		accident_key INT PRIMARY KEY,
		accident_time TIME,
		environment VARCHAR,
		road_surface VARCHAR,
		traffic_control VARCHAR,
		visibility VARCHAR,
		impact_type VARCHAR)
	""",
	"""
	CREATE TABLE weather(
		weather_key INT PRIMARY KEY,
		station_name VARCHAR,
		longitude INT,
		latitude INT,
		temperature INT,
		visibility VARCHAR,
		wind_speed INT,
		wind_chill INT,
		wind_direction VARCHAR,
		pressure INT
		)
	""",
	"""
	CREATE TABLE event(
		event_key INT PRIMARY KEY,
		event_name VARCHAR,
		event_start_date DATE,
		event_end_date DATE)
	""",
	"""
	CREATE TABLE location(
		location_key INT PRIMARY KEY,
		streetName_highway VARCHAR,
		intersection1_offramp1 VARCHAR,
		intersection2_offramp2 VARCHAR,
		longitude decimal,
		latitude decimal,
		neighborhood VARCHAR)
	""",
	"""
	CREATE TABLE accidentFact(
		hour_key INTEGER NOT NULL,
		location_key INTEGER NOT NULL,
		accident_key INTEGER NOT NULL,
		weather_key INTEGER NOT NULL,
		event_key INTEGER NOT NULL,
		PRIMARY KEY (hour_key, location_key, accident_key, weather_key, event_key),
		FOREIGN KEY(hour_key) REFERENCES hour(hour_key) ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY(location_key) REFERENCES location(location_key) ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY(accident_key) REFERENCES accident(accident_key) ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY(weather_key) REFERENCES weather(weather_key) ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY(event_key) REFERENCES event(event_key) ON UPDATE CASCADE ON DELETE CASCADE,
		is_fatal VARCHAR,
		is_intersection VARCHAR)
	"""
	]

def create():
	with open("creds.json", 'r') as f:
		creds = json.load(f)
	conn=None
	try:
		conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
		cursor = conn.cursor()
		cursor.execute("DROP TABLE accidentFact;")
		cursor.execute("DROP TABLE accident;")
		cursor.execute("DROP TABLE hour;")
		cursor.execute("DROP TABLE location;")
		cursor.execute("DROP TABLE weather;")
		cursor.execute("DROP TABLE event;")
		
		for table in CREATETABLES:
			cursor.execute(table)
		cursor.close()
		conn.commit()
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

create()















