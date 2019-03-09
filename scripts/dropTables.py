import psycopg2
import json

def drop_tables():
	with open("creds.json", 'r') as f:
		creds = json.load(f)
	conn=None
	try:
		conn = psycopg2.connect(host=creds["host"],database=creds["database"], user=creds["user"], password=creds["password"])
		cursor = conn.cursor()
		cursor.execute("DROP TABLE accident;")
		cursor.execute("DROP TABLE hour;")
		cursor.execute("DROP TABLE location;")
		cursor.execute("DROP TABLE weather;")
		cursor.execute("DROP TABLE event;")
		cursor.execute("DROP TABLE accidentFact;")
		cursor.close()
		conn.commit()
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()