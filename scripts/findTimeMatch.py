import re
import os
import pandas as pd
import csv


CHUNKED_WEATHER_DIR = './data/cleaned/weather/ottawa-chunked'
OUTPUT_DIR = './data/cleaned/fact'
COLLISION_DIR = './data/cleaned/accident-dim'


def main():
    # Run location check
    if os.getcwd().split('/')[-1] != 'csi4142':
        print('Run this file from the root directory of the project.')
        return

    collision_files = [f'{COLLISION_DIR}/{x}' for x in os.listdir(COLLISION_DIR)]

    for collision_file in collision_files:
        year = collision_file.split('/')[-1][16:-4]
        create_fact_year(collision_file, year)

    # year = collision_files[0].split('/')[-1][16:-4]
    # create_fact_year(collision_files[0], year)


def create_fact_year(collision_file, year):
    field_names = ['HOUR_KEY', 'LOCATION_KEY', 'ACCIDENT_KEY', 'WEATHER_KEY', 'IS_FATAL', 'IS_INTERSECTION']
    print(f'Creating fact table: year {year}')
    reader = csv.DictReader(open(collision_file, 'r'))
    writer = csv.DictWriter(open(f'{OUTPUT_DIR}/fact{year}.csv', 'w'), fieldnames=field_names)
    writer.writeheader()

    index = 0

    for row in reader:
        if index % 100 == 0:
            print(f'Done {index} lines...')

        weather_id = find_weather_id(row['ACCIDENT_TIME'], row['DATE'], row['CLOSEST_STATION'])
        if weather_id is not False:
            new_row = {
                'HOUR_KEY': row['HOUR_KEY'],
                'LOCATION_KEY': row['LOCATION_KEY'],
                'ACCIDENT_KEY': row['ACCIDENT_KEY'],
                'WEATHER_KEY': weather_id,
                'IS_FATAL': row['IS_FATAL'],
                'IS_INTERSECTION': row['IS_INTERSECTION']
            }
            writer.writerow(new_row)
        else:
            print('Something went wrong', row)

        index += 1


def find_weather_id(coll_time, coll_date, closest_station):
    closest_station_dir = f"{CHUNKED_WEATHER_DIR}/{closest_station.lower().replace(' ', '-')}"
    station_files = [f'{closest_station_dir}/{x}' for x in os.listdir(closest_station_dir)]
    coll_date_time = f'{coll_date} {coll_time}'

    for station_file in station_files:
        df = pd.read_csv(station_file, engine='python', encoding='utf-8-sig')
        df = df[((df['X.Date.Time'] == coll_date_time) & (df['X.U.FEFF..Station.Name.'] == closest_station))]
        if not df.empty:
            try:
                return df['weatherID'].values[0]
            except:
                # return df['weatherID'][0].item()
                print(station_file)
                print(df['weatherID'])
    return False


if __name__ == '__main__':
    main()
