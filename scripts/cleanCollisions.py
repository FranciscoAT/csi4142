import argparse
import csv
import sys
import os
import collections
import datetime

# Constants
DATA_DIR = './data'
SOURCE_DIR = f"{DATA_DIR}/source/collision"
CLEAN_DIR = f"{DATA_DIR}/cleaned/accident-dim"
GARBAGE_DIR = f"{DATA_DIR}/garbage"
ACCIDENT_FILE = f"{CLEAN_DIR}/accident-dim.txt"
GARBAGE_FILE_ACC = f"{GARBAGE_DIR}/accident-dim.txt"
GARBAGE_FILE_COLL = f'{GARBAGE_DIR}/collision.txt'


def main() -> None:
    # Run location check
    if os.getcwd().split('/')[-1] != 'csi4142':
        print('Run this file from the root directory of the project.')
        return

    csv_files = sorted(os.listdir(SOURCE_DIR))

    accident_index = 0
    location_index = 0
    locations = {}
    for csv_file in csv_files:
        if '2017' in csv_file:
            print(f"Ignoring {csv_file}")
            continue

        print(f"Cleaning {csv_file}...")
        accident_index, location_index, locations = clean_file(csv_file, accident_index, location_index, locations)


def clean_file(filename, accident_index, location_index, locations):
    field_names = [
        "ACCIDENT_ID",
        "LOCATION",
        "LONGITUDE",
        "LATITUDE",
        "DATE",
        "TIME",
        "LOCATION_ID"
    ]

    reader = csv.DictReader(open(f"{SOURCE_DIR}/{filename}"))
    writer = csv.DictWriter(open(f"{CLEAN_DIR}/{filename}", 'w'), fieldnames=field_names)
    writer.writeheader()

    for row in reader:
        # Accident ID
        new_row = get_elements(row)
        new_row["ACCIDENT_ID"] = accident_index
        accident_index += 1

        # Location ID
        new_location = f"{new_row['LONGITUDE']}-{new_row['LATITUDE']}"
        if new_location not in locations:
            locations[new_location] = location_index
            new_row["LOCATION_ID"] = location_index
            location_index += 1
        else:
            new_row["LOCATION_ID"] = locations[new_location]

        # Clean Time
        new_row["TIME"], next_day = parse_time(new_row["TIME"])

        if next_day:
            new_date = datetime.datetime.strptime(new_row["DATE"], "%Y-%m-%d")
            new_date = new_date + datetime.timedelta(days=1)
            new_row["DATE"] = new_date.strftime("%Y-%m-%d")

        # Write row to file
        writer.writerow(new_row)

    return accident_index, location_index, locations

def parse_time(time_in):
    if len(time_in.split(':')[0]) == 1:
        time_in = f"0{time_in}"

    new_time = convert24(time_in)

    hours, minutes, _ = [int(x) for x in new_time.split(':')]

    if minutes >= 30:
        hours += 1

    if hours == 24:
        return "00:00", True
    elif hours < 10:
        return f"0{hours}:00", False
    else:
        return f"{hours}:00", False

def convert24(time_in):
    if time_in[-2:] == "AM" and time_in[:2] == "12":
        return "00" + time_in[2:-2]
    elif time_in[-2:] == "AM":
        return time_in[:-2]
    elif time_in[-2:] == "PM" and time_in[:2] == "12":
        return time_in[:-2]
    else:
        return str(int(time_in[:2]) + 12) + time_in[2:8]


def get_elements(row):
    elements = [
        "LOCATION",
        "LONGITUDE",
        "LATITUDE",
        "DATE",
        "TIME"
    ]

    new_row = {}
    for key in elements:
        new_row[key] = row[key]

    return new_row


if __name__ == "__main__":
    main()
