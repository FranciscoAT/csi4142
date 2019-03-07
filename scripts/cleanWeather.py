import csv, os
import pandas as pd

def getWeatherData(city):
	ChunkSize = 1000000
	SOURCE_DIR = '../data/source/weather'
	STATION_DIR = '../data/cleaned/stations/'
	WEATHER_DIR = '../data/cleaned/weather/'+city+'/'

	station_file = ''
	if(city == 'Calgary'):
		station_file = 'Calgary_Stations.csv'
	elif(city == 'Ottawa'):
		station_file = 'Ottawa_Stations.csv'
	elif(city == 'Toronto'):
		station_file = 'Toronto_Stations.csv'
	else:
		print('Invalid City')
		exit()

	df = pd.read_csv(STATION_DIR+station_file, engine='python', encoding="utf-8-sig")
	stations = df['Name'].tolist()
	files = sorted([f"{SOURCE_DIR}/{x}" for x in os.listdir(SOURCE_DIR)])
	z = 0
	for file in files:
		print("Checking file "+file)
		for chunk in pd.read_csv(file, chunksize=ChunkSize):
			print("Chunky AF ... ", z)
			x = chunk[chunk['X.U.FEFF..Station.Name.'].isin(stations)]
			if x.size > 0:
				x.to_csv(WEATHER_DIR+city+'_Chunk'+str(z)+'_weather.csv', encoding='utf-8', index=False)
				z+=1
getWeatherData('Toronto')
getWeatherData('Ottawa')