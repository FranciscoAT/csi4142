import re, os, pandas as pd , csv

WEATHER_DIR = '../data/cleaned/weather/ottawa/'
COLLISION_DIR = '../data/cleaned/accident-dim/'
OUTPUT_DIR = '../data/cleaned/fact/'

def main():
	collision_files = [f'{COLLISION_DIR}{x}' for x in os.listdir(COLLISION_DIR)]
	weather_files = [f'{WEATHER_DIR}{x}' for x in os.listdir(WEATHER_DIR)]
	for collision_file in collision_files:
		find_weather_ids(weather_files, collision_file)

def find_weather_ids(weather_files, collision_file):
	field_names = ['HOUR_KEY','LOCATION_KEY','ACCIDENT_KEY','WEATHER_KEY','IS_FATAL','IS_INTERSECTION']
	year = collision_file.split('/')[-1][16:-4]
	writer = csv.DictWriter(open(f'{OUTPUT_DIR}fact{year}.csv', 'w'),fieldnames = field_names)
	writer.writeheader()
	reader = csv.DictReader(open(collision_file, 'r'))
	for row in reader:
		weatherId = find_weather_id(weather_files, row)
		if weatherId is not False:
			print(weatherId)
			new_row = {
				'HOUR_KEY': row['HOUR_KEY'],
				'LOCATION_KEY': row['LOCATION_KEY'],
				'ACCIDENT_KEY': row['ACCIDENT_KEY'],
				'WEATHER_KEY': weatherId,
				'IS_FATAL': row['IS_FATAL'],
				'IS_INTERSECTION': row['IS_INTERSECTION']
			}
			writer.writerow(new_row)
		else:
			print("Something went wrong: ", row)


def find_weather_id(files, row):
	date_time = f'{row["DATE"]} {row["ACCIDENT_TIME"]}'
	for file in files:
		df = pd.read_csv(file, engine='python', encoding="utf-8-sig")		
		df = df[((df['X.Date.Time'] == date_time) & (df['X.U.FEFF..Station.Name.'] == row['CLOSEST_STATION']))]
		if not df.empty:
			return df['weatherID'].item()
	return False

main()
