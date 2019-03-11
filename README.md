# CSI4142 Intro. To Data Science

--------

## Table of Contents

1. [Members](#group-members)
1. [Dates](#important-dates)

--------

## Group Members

- Francisco Trindade 7791605
- Mac Hayter 8256068
- Reyna Doerwald 8216389

--------

## Important Dates

- Feb 5: Conceptual Design
- March 1: Midterm
- March 12: Physical Design
- April 2: BI Dashboard

--------

https://drive.google.com/open?id=1d7SsIr_iLYkrwJMSTDzIgIGY9LRiqtCK

# data folder structure

```
data
  \ --- source
        \ --- collision
              \ --- *unzip collisions.zip here*
        \ --- neighborhood
              \ --- *put neighborhood_list.txt here*
        \ --- stations
              \ --- *put Station Inventory EN.csv here and remove the rows above the header*
        \ --- weather
              \ --- *put weather files from class drive here*
  \ --- cleaned
        \ --- accident-dim
              \ --- *collision data inserted here after running scripts/cleanCollisions.py*
        \ --- fact
              \ --- *unzip fact.zip or run scripts/findTimeMatch.py*
        \ --- hour
              \ --- *run scripts/cleanHour.py*
        \ --- neighborhood
              \ --- *put neighborhood_list.json here, or run generateNeighborhoods.py*
        \ --- stations
              \ --- *stations directory, run scripts/cleanStations.py*
        \ --- weather
              \ --- Ottawa
                  \ --- *chunked Ottawa weather data, run scripts/cleanWeather.py*
                  \ --- ottawa-chunked
                        \ --- *chunked Ottawa weather data by station, run scripts/doubleChunk.py*
              \ --- toronto
                  \ --- *chunked Toronto weather data, run script/cleanWeather.py*
```

## Order or running stuff

This assumes everything is put in the source directory!!

1. Run `scripts/cleanHour.py`, this generates the hour csvs by year
1. Run `scripts/generateNeighborhoods.py`, this generates the lat/long of all neighborhoods defined in `neighborhood_list.txt`
1. Run `scripts/cleanWeather.py`, cleans up all the weather data and puts it under `source/Ottawa` and `source/Tronto` chunked
1. Run `scripts/doubleChunk.py`, rechunks the Ottawa data by weather station, puts it all under `source/Ottawa/ottawa-chunked`
1. Run `scripts/nonMatchingStations.py`, finds all stations specified in `.../ottawa-chunked` and compares it against those under `neighborhood_list.json` then only keeps the wanted ones
1. Run `scripts/cleanCollisions.py`, uses all of the above generated data to clean up accidents, matching them with a location id, nearest station, accident ID, hour ID,  along with other data
1. Run `scripts/findTimeMatch.py`, matches each accident ID to a weather ID
1. Upload data to DB using `scripts/createTables.py`, `scripts/addData.py`