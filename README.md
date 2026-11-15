<<<<<<< HEAD
# Project 5: Brevet time calculator with Ajax and MongoDB

Simple list of controle times from project 4 stored in MongoDB database.

## What is in this repository

You have a minimal implementation of Docker compose in DockerMongo folder, using which you can connect the flask app to MongoDB (as demonstrated in class). Refer to the lecture slide `05a-Table-driven.pdf` and `05b-Docker-Compose.pdf`. You'll also need MongoCommands.txt. Solved acp_times.py file is in Canvas! 

## Functionality you'll add

You will reuse *your* code from project 4 (https://bitbucket.org/UOCIS322/proj4-brevets/). Recall: you created a list of open and close controle times using AJAX. In this project, you will create the following functionalities.

1. Create two buttons "Submit" and "Display" in the page where have controle times.
2. On clicking the Submit button, the control times should be entered into the database.
3. On clicking the Display button, the entries from the database should be displayed in a new page.

Handle error cases appropriately. For example, Submit should return an error if there are no controle times. One can imagine many such cases: you'll come up with as many cases as possible.

## Tasks

* Submit a working application.
* A README.md file that includes not only identifying information (your name) but but also a revised, clear specification 
  of the brevet controle time calculation rules.
* Dockerfile
* Test cases for the two buttons. No need to run nose.
* docker-compose.yml

### You'll turn in your credentials.ini from which we will get the following:

* `author`
* `repo`

All must be under the section `[DEFAULT]`.

## Grading Rubric

* If your code works as expected: 100 points. This includes:
	* AJAX in the frontend. That is, open and close times are automatically populated, 
	* Frontend to backend interaction (with correct requests/responses), 
	* README is updated with your name and email.
* If the AJAX logic is not working, 10 points will be docked off. 
* If the README is not clear or missing, up to 15 points will be docked off. 
* If the two test cases fail, up to 15 points will be docked off.
* If the logic to enter into or retrieve from the database is wrong, 30 points will be docked off.
* If none of the functionalities work, 30 points will be given assuming 
    * The credentials.ini is submitted with the correct URL of your repo, and
    * Dockerfile is present 
    * Docker-compose.yml works/builds without any errors
* If the Docker-compose.yml doesn't build or is missing, 10 points will be docked off.
* If credentials.ini is missing, 0 will be assigned.
=======
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
>>>>>>> 739cf67 (Project 5: MongoDB submit and display)
