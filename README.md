# Project 5: Brevet Time Calculator with Ajax and MongoDB

**Author:** Canyon DeLong
**Email:** canyond@uoregon.edu

## Overview
A web calculator for ACP-sanctioned brevets (200-1000 km). Open and close
times are filled in automatically through AJAX calls to a Flask backend.
Two buttons store the results in MongoDB and show them again:

* **Submit** - sends every filled-in control row to the server, which replaces
  the previously stored data and saves the new rows in MongoDB. Each Submit
  overwrites the old data, so pressing it twice never creates duplicates.
* **Display** - opens a new page listing everything stored in the database.

### Error handling
* Submit with no controls entered -> error message, nothing saved.
* Submit with a row whose open/close time is missing or whose distance is not a number -> error message, nothing saved.
* Display with an empty database -> "No controle times have been submitted yet."
* Database unreachable -> a clean error message instead of a crash.

## Running
```
cd DockerMongo
docker compose up --build
```
Then open http://localhost:5001

## Tests
With the containers running:
```
docker compose exec web python tests.py
```

## Brevet control time rules (ACP / RUSA)
Opening time = control distance divided by the **maximum** speed.
Closing time = control distance divided by the **minimum** speed.
When the control spans several segments, the time for each segment is added up.

| Control segment (km) | Min speed (km/h) | Max speed (km/h) |
|----------------------|------------------|------------------|
| 0 - 200              | 15               | 34               |
| 200 - 400            | 15               | 32               |
| 400 - 600            | 15               | 30               |
| 600 - 1000           | 11.428           | 28               |

Example: a control at 350 km opens after 200/34 + 150/32 hours, and
closes after 350/15 hours.

Special cases:
* The start control (0 km) opens at the start time and closes 1 hour later.
* Controls within the first 60 km use the "French" closing rule: distance/20 + 1 hour.
* A control may be up to 20% beyond the brevet distance. A control at or
  past the brevet distance is treated as the finish: it opens by the brevet
  distance's max-speed time and closes at the fixed limit
  (200 km: 13h30, 300 km: 20h, 400 km: 27h, 600 km: 40h, 1000 km: 75h).
* Times are rounded to the nearest minute.
