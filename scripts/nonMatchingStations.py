import csv
import os

OTTAWA_CHUNKED_DIR = './data/cleaned/weather/ottawa-chunked'
STATIONS_DIR = './data/cleaned/stations'
OTTAWA_STATIONS = f'{STATIONS_DIR}/Ottawa_Stations.csv'
OUTPUT_FILE = f'{STATIONS_DIR}/cleaned_ottawa_stations.csv'

def main():
    if os.getcwd().split('/')[-1] != 'csi4142':
        print('Run this file from the root directory of the project.')
        return

    field_names = [
        "NAME",
        "LAT",
        "LNG"
    ]

    reader = csv.DictReader(open(OTTAWA_STATIONS, 'r'))
    writer = csv.DictWriter(open(OUTPUT_FILE, 'w'), fieldnames=field_names)
    writer.writeheader()
    found_stations = os.listdir(OTTAWA_CHUNKED_DIR)
    
    for row in reader:
        if row['Name'].lower().replace(' ', '-') in found_stations:
            new_row = {
                "NAME": row['Name'],
                "LAT": row['Latitude (Decimal Degrees)'],
                "LNG": row['Longitude (Decimal Degrees)']
            }
            writer.writerow(new_row)

if __name__ == '__main__':
    main()

