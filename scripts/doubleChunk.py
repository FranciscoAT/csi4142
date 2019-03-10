import csv
import os
import pandas as pd

OTTAWA_WEATHER_DIR = './data/cleaned/weather/Ottawa'
OTTAWA_CHUNKED_DIR = './data/cleaned/weather/ottawa-chunked'


def main():
    # Run location check
    if os.getcwd().split('/')[-1] != 'csi4142':
        print('Run this file from the root directory of the project.')
        return
    chunked_files = [f'{OTTAWA_WEATHER_DIR}/{x}' for x in os.listdir(OTTAWA_WEATHER_DIR)]

    for chunked_file in chunked_files:
        double_chunk(chunked_file)


def double_chunk(chunked_file):
    print(f'Double Chunking {chunked_file}')
    df = pd.read_csv(chunked_file, engine='python', encoding='utf-8-sig')
    stations = set(df['X.U.FEFF..Station.Name.'].tolist())
    wanted_years = ['2013', '2014', '2015', '2016', '2017', '2018']

    for station in stations:
        stations_rows = df[(df['X.U.FEFF..Station.Name.'] == station)]
        stations_rows = stations_rows[(stations_rows['Year'].isin(wanted_years))]
        new_path_name = f'{OTTAWA_CHUNKED_DIR}/{station.lower().replace(" ", "-")}'
        if not os.path.exists(new_path_name):
            os.makedirs(new_path_name)
        new_file_name = f'{new_path_name}/{chunked_file.split("/")[-1]}'
        open(new_file_name, 'w').close()
        print(f'Writing station {station} to double chunked file {new_file_name}')
        stations_rows.to_csv(new_file_name, encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
