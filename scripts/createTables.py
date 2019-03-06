import psycopg2
#from config import config

CREATETABLES = (
	"""
	CREATE TABLE hour (
		hour_key SERIAL PRIMARY KEY,
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
		accident_key SERIAL PRIMARY KEY,
		accident_time TIME,
		environment VARCHAR,
		road_surface VARCHAR,
		traffic_control VARCHAR,
		visibility VARCHAR,
		impact_type VARCHAR)
	""",
	"""
	CREATE TABLE weather(
		weather_key SERIAL PRIMARY KEY,
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
		event_key SERIAL PRIMARY KEY,
		event_name VARCHAR,
		event_start_date DATE,
		event_end_date DATE)
	""",
	"""
	CREATE TABLE location(
		location_key SERIAL PRIMARY KEY,
		streetName_highway VARCHAR,
		intersection1_offramp1 VARCHAR,
		intersection2_offramp2 VARCHAR,
		longitude decimal,
		latitude decimal,
		neighborhood VARCHAR)
	""",
	"""
	CREATE TABLE accidentFact(
		FOREIGN KEY(hour_key) REFERENCES hour(hour_key),
		FOREIGN KEY(location_key) REFERENCES location(location_key),
		FOREIGN KEY(accident_key) REFERENCES accident(accident_key),
		FOREIGN KEY(weather_key) REFERENCES weather(weather_key),
		FOREIGN KEY(event_key) REFERENCES event(event_key),
		is_fatal VARCHAR,
		is_intersection VARCHAR)
	"""
	)

def create():
	conn=None
	try:
		conn = psycopg2.connect(host="138.197.141.138",database="dataScience", user="reyna", password="rey452")
		cursor = conn.cursor()
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















