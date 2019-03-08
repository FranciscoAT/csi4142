import csv, os
import pandas as pd
import geopy.distance

def distanceFromOttawa(row):
	coords_1 = (45.41, -75.7) #Latitude and Longitude of Ottawa
	coords_2 = (row['Latitude (Decimal Degrees)'],row['Longitude (Decimal Degrees)'])
	distance = geopy.distance.vincenty(coords_1, coords_2).km
	return distance

def distanceFromToronto(row):
	coords_1 = (43.7, -79.42) #Latitude and Longitude of Toronto
	coords_2 = (row['Latitude (Decimal Degrees)'],row['Longitude (Decimal Degrees)'])
	distance = geopy.distance.vincenty(coords_1, coords_2).km
	return distance

def distanceFromCalgary(row):
	coords_1 = (51.05011, -114.08529) #Latitude and Longitude of Calgary
	coords_2 = (row['Latitude (Decimal Degrees)'],row['Longitude (Decimal Degrees)'])
	distance = geopy.distance.vincenty(coords_1, coords_2).km
	return distance

def getStations(distance):
	CLEAN_PATH = '../data/cleaned/stations/'
	df = pd.read_csv('../data/source/stations/Station Inventory EN.csv', engine='python', encoding="utf-8-sig")
	df['Ottawa_Dist'] = df.apply(distanceFromOttawa, axis=1) 
	#df['Toronto_Dist'] = df.apply(distanceFromToronto, axis=1) 
	#df['Calgary_Dist'] = df.apply(distanceFromCalgary, axis=1) 
	df_Ottawa = df[(df.Ottawa_Dist <= distance)]
	#df_Toronto = df[(df.Toronto_Dist <= distance)]
	#df_Calgary = df[(df.Calgary_Dist <= distance)]
	df_Ottawa.to_csv(CLEAN_PATH+'Ottawa_Stations.csv', encoding='utf-8', index=False)
	#df_Toronto.to_csv(CLEAN_PATH+'Toronto_Stations.csv', encoding='utf-8', index=False)
	#df_Calgary.to_csv(CLEAN_PATH+'Calgary_Stations.csv', encoding='utf-8', index=False)

getStations(50)