import argparse
import csv
import sys
import os
import collections

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

    csv_files = sorted([f"{SOURCE_DIR}/{x}" for x in os.listdir(SOURCE_DIR)])

    # Clean files
    open(ACCIDENT_FILE, 'w').close()
    open(GARBAGE_FILE_ACC, 'w').close()
    open(GARBAGE_FILE_COLL, 'w').close()

    for csv_file in csv_files:
        if '2017' in csv_file:
            print(f"Ignoring {csv_file}")
            continue

        print(f"Cleaning {csv_file}...")
        reader = csv.DictReader(open(csv_file))
        clean_collision(reader)


def clean_collision(reader):
    reqd_headers = [
        'TIME',
        'ENVIRONMENT',
        'SURFACE_CONDITION',
        'TRAFFIC_CONTROL',
        'LIGHT',
        'IMPACT_TYPE'
    ]

    clean_rows = []
    garbage_rows = []
    print("Initial Row Cleaning...")
    for row in reader:
        new_row, rejected = check_row(row, reqd_headers)
        if rejected:
            garbage_rows.append(new_row)
        else:
            clean_rows.append(new_row)
    print(f'Rejected {len(garbage_rows)} rows in initial collision check')
    append_to(GARBAGE_FILE_COLL, garbage_rows)

    print('Cleaning accident dim...')
    clean_accident_dim(clean_rows)


def clean_accident_dim(rows):
    # Headers
    time = 'TIME'
    environment = 'ENVIRONMENT'
    condition = 'SURFACE_CONDITION'
    control = 'TRAFFIC_CONTROL'
    visibility = 'LIGHT'
    impact = 'IMPACT_TYPE'

    wanted_headers = [
        'TIME',
        'ENVIRONMENT',
        'SURFACE_CONDITION',
        'TRAFFIC_CONTROL',
        'LIGHT',
        'IMPACT_TYPE'
    ]

    index = len(list(csv.DictReader(open(ACCIDENT_FILE))))

    parsed_rows = []
    rejected_rows = []
    environment_types = set()
    for row in rows:
        new_row, _ = check_row(row, wanted_headers)
        new_row["id"] = index
        index += 1
        environment_types.add(new_row[environment])
        parsed_rows.append(new_row)

    print(f'Rejected {len(rejected_rows)} in accident dimension')
    append_to(ACCIDENT_FILE, parsed_rows)
    append_to(GARBAGE_FILE_ACC, rejected_rows)
    # print(environment_types)


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
