import os
import json
import requests

SOURCE_FILE = './data/source/neighborhood/neighborhood_list.txt'
OUTPUT_FILE = './data/cleaned/neighborhood/neighborhood_list.json'
CREDS_FILE = './scripts/creds.json'
KEY = json.load(open(CREDS_FILE, 'r'))["key"]


def main():
    # Run location check
    if os.getcwd().split('/')[-1] != 'csi4142':
        print('Run this file from the root directory of the project.')
        return

    location_names = []
    with open(SOURCE_FILE, 'r') as in_file:
        for hood in in_file:
            location_names.append(hood.rstrip())

    location_output = {}
    for location in location_names:
        lat_long = query(location)

        if lat_long == False:
            print(f'Retrying with appended Ottawa...')
            lat_long = query(f'{location} Ottawa')

        if lat_long != False:
            location_output[location] = lat_long

    with open(OUTPUT_FILE, 'w') as out_file:
        json.dump(location_output, out_file, sort_keys=True, indent=2)


def query(location):
    print(f'Querying for {location}')
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    location_query = location.replace(' ', '%20')
    full_url = f"{url}?input={location_query}&key={KEY}&fields=geometry&inputtype=textquery"

    r = requests.get(url=full_url)
    data = r.json()

    if len(data['candidates']) == 0:
        print(f'Something went wrong query for {location}', data)
        return False

    return data['candidates'][0]['geometry']['location']


if __name__ == '__main__':
    main()
