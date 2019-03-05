import argparse
import csv
import sys
import os
import collections

# Constants
DATA_DIR = './data'
SOURCE_DIR = f"{DATA_DIR}/source/collision"
CLEAN_DIR = f"{DATA_DIR}/cleaned/accident-dim"
GARBAGE_DIR = f"{DATA_DIR}/garbage/accident-dim"
ACCIDENT_FILE = f"{CLEAN_DIR}/accident-dim.txt"
GARBAGE_FILE = f"{GARBAGE_DIR}/accident-dim.txt"


def main() -> None:
    # Run location check
    if os.getcwd().split('/')[-1] != 'csi4142':
        print('Run this file from the root directory of the project.')
        return

    csv_files = [f"{SOURCE_DIR}/{x}" for x in os.listdir(SOURCE_DIR)]
    # Order is important
    csv_files.sort()
    print(csv_files)

    # Clean files
    open(ACCIDENT_FILE, 'w').close()
    open(GARBAGE_FILE, 'w').close()

    for csv_file in csv_files:
        if '2017' in csv_file:
            print(f"Ignoring {csv_file}")
            continue

        print(f"Cleaning {csv_file}...")
        reader = csv.DictReader(open(csv_file))
        clean_collision(reader)


def clean_collision(reader):
    clean_accident_dim(reader)


def clean_accident_dim(reader):
    # Headers
    time = 'TIME'
    environment = 'ENVIRONMENT'
    condition = 'SURFACE_CONDITION'
    control = 'TRAFFIC_CONTROL'
    visibility = 'LIGHT'
    impact = 'IMPACT_TYPE'

    reqd_headers = [
        time,
        environment,
        condition,
        control,
        visibility,
        impact
    ]

    index = len(list(csv.DictReader(open(ACCIDENT_FILE))))

    parsed_rows = []
    rejected_rows = []
    environment_types = set()
    for row in reader:
        new_row, rejected = check_row(row, reqd_headers)
        new_row["id"] = index
        index += 1
        environment_types.add(new_row[environment])

        if rejected:
            rejected_rows.append(new_row)
        else:
            parsed_rows.append(new_row)

    append_to(ACCIDENT_FILE, parsed_rows)
    append_to(GARBAGE_FILE, rejected_rows)
    print(environment_types)


def check_row(row, headers):
    new_row = {}
    rejected = False
    for header in headers:
        if row[header] == '':
            rejected = True
        new_row[header] = row[header]
    return new_row, rejected
    

def compress_row(row):
    compressed_row = []
    for _, val in row.items():
        compressed_row.append(val)
    return ','.join(compressed_row)

def append_to(filename, rows):
    with open(filename, 'a') as app_file:
        for row in rows:
            app_file.write(f"{str(row)}\n")


if __name__ == "__main__":
    main()
