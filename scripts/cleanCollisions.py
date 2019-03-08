import argparse
import csv
import sys
import os
import collections
import datetime
import json
import math

# Constants
DATA_DIR = './data'
SOURCE_DIR = f"{DATA_DIR}/source/collision"
CLEAN_DIR = f"{DATA_DIR}/cleaned/accident-dim"
NEIGHBORHOODS = f"{DATA_DIR}/cleaned/neighborhood/neighborhood_list.json"


def main() -> None:
    # Run location check
    if os.getcwd().split('/')[-1] != 'csi4142':
        print('Run this file from the root directory of the project.')
        return

    print("Please ensure you have run scripts/generateNeighborhoods.py before running this else it will fail!")

    clean_ottawa_collisions()


def clean_ottawa_collisions():
    print("Cleaning Ottawa Collisions")
    hood_json = json.load(open(NEIGHBORHOODS, 'r'))

    csv_files_raw = os.listdir(SOURCE_DIR)
    csv_files = []
    for file in csv_files_raw:
        if 'ottawa' in file.lower():
            csv_files.append(file)

    csv_files = sorted(csv_files)

    accident_index = 0
    location_index = 0
    locations = {}
    for csv_file in csv_files:
        is_2017 = False
        if '2017' in csv_file:
            is_2017 = True

        print(f"Cleaning {csv_file}...")
        accident_index, location_index, locations = clean_file(
            csv_file, accident_index, location_index, locations, is_2017, hood_json)


def clean_file(filename, accident_index, location_index, locations, is_2017, hood_json):
    core_field_names = [
        "LOCATION",
        "LONGITUDE",
        "LATITUDE",
        "DATE",
        "TIME",
        "ENVIRONMENT",
        "SURFACE_CONDITION",
        "TRAFFIC_CONTROL",
        "LIGHT",
        "IMPACT_TYPE",
        "COLLISION_CLASSIFICATION"
    ]

    field_names = [
        "ACCIDENT_KEY",
        "ACCIDENT_TIME",
        "ENVIRONMENT",
        "ROAD_SURFACE",
        "TRAFFIC_CONTROL",
        "VISIBILITY",
        "IMPACT_TYPE",
        "LOCATION_KEY",
        "LOCATION",
        "LONGITUDE",
        "LATITUDE",
        "DATE",
        "IS_FATAL",
        "IS_INTERSECTION",
        "ROAD_HIGHWAY",
        "INTERSECTION_RAMP_1",
        "INTERSECTION_RAMP_2",
        "NEIGHBORHOOD"
    ]

    reader = csv.DictReader(open(f"{SOURCE_DIR}/{filename}"))
    writer = csv.DictWriter(open(f"{CLEAN_DIR}/{filename}", 'w'), fieldnames=field_names)
    writer.writeheader()

    for row in reader:
        # Accident ID
        new_row = get_elements(row, core_field_names)
        new_row["ACCIDENT_KEY"] = accident_index
        accident_index += 1

        # Rename Keys
        new_row["ACCIDENT_TIME"] = new_row.pop("TIME")
        new_row["ROAD_SURFACE"] = new_row.pop("SURFACE_CONDITION")
        new_row["VISIBILITY"] = new_row.pop("LIGHT")

        # Location ID
        new_location = f"{new_row['LONGITUDE']}-{new_row['LATITUDE']}"
        if new_location not in locations:
            locations[new_location] = location_index
            new_row["LOCATION_KEY"] = location_index
            location_index += 1
        else:
            new_row["LOCATION_KEY"] = locations[new_location]

        # Clean Time
        new_row["ACCIDENT_TIME"], next_day = parse_time(new_row["ACCIDENT_TIME"])

        new_row["DATE"] = normalize_date(new_row["DATE"], next_day, is_2017)

        # Determine fatality
        if " fatal injury" in new_row["COLLISION_CLASSIFICATION"].lower():
            new_row["IS_FATAL"] = True
        else:
            new_row["IS_FATAL"] = False

        # Clean up unnecesary ids from source
        for key in ["ENVIRONMENT", "ROAD_SURFACE", "TRAFFIC_CONTROL", "VISIBILITY", "IMPACT_TYPE"]:
            new_row[key] = parse_out_id(new_row[key])

        # Clean up location
        # parse_location(new_row["LOCATION"])

        # Get Neighborhood
        new_row["NEIGHBORHOOD"] = getNeighborhood(new_row["LATITUDE"], new_row["LONGITUDE"], hood_json)

        # Remove some keys
        new_row.pop("COLLISION_CLASSIFICATION")

        # Write row to file
        writer.writerow(new_row)

    return accident_index, location_index, locations


def getNeighborhood(lat, long, hood_json):
    closest = ''
    closest_val = 1000000

    for key, value in hood_json.items():
        dist = distance((float(lat), float(long)), (value['lat'], value['lng']))
        if dist < closest_val:
            closest_val = dist
            closest = key
    return closest


def distance(x, y):
    lat1, lon1 = x
    lat2, lon2 = y
    radius = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon2)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


def parse_location(location):
    is_intersection = False
    road_highway_name = ''
    intersection_ramp_1 = ''
    intersection_ramp_2 = ''

    if '@' in location:
        is_intersection = True
        location = location.split('@')
        if '/' in location[0] and '/' in location[1]:
            print('@'.join(location))


def normalize_date(date, next_day, is_2017):
    if next_day == False and is_2017 == False:
        return date

    in_format = "%Y-%m-%d"
    if is_2017:
        in_format = "%m/%d/%Y"

    new_date = datetime.datetime.strptime(date, in_format)

    if next_day:
        new_date = new_date + datetime.timedelta(days=1)

    return new_date.strftime("%Y-%m-%d")


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


def parse_out_id(val_in):
    if val_in == '':
        return ''
    return val_in.split(' - ')[1]


def get_elements(row, field_names):
    new_row = {}
    for key in field_names:
        new_row[key] = row[key]

    return new_row


if __name__ == "__main__":
    main()
