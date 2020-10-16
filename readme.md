# Traffomatic

## Problem Statement

Create a solution for the problem of traffic congestion at traffic junction stop-lights and hence reduce traffic congestion on roads.

### Technology Stack

- Flask

- MongoDB

### Deployed Project's Backend server

`https://traffic-congestion.herokuapp.com/`<br><br>

## Instructions to install

1\. Clone this repository:

`git clone https://github.com/Sourabhtripathi/Adverb-Submission---Traffic-Congestion`

2\. Change directory

`cd Traffic-Congestion-api/server`

3\. Install dependencies

`pip install requirements.txt`

4\. Generate Authentication Key for Distance Matrix API.

Refer to this link - <https://distancematrix.ai>

5\. Generate MongoDB database URI.

Refer to this link - <https://www.mongodb.com/cloud/atlas>

6\. Create a .env file and add the mentioned details in it.

```
# specify flask app's python file
FLASK_APP = app.py

# specify MongoDB database URI
MONGODB_URI = URI TO CONNECT TO DATABASE

# specify Distance Matrix API key
API_KEY = API KEY

```

7\. Start the server

`flask run`<br><br>

## Routes

### 1\. "http://localhost:5000/junctions" [GET] To get list of all junction's data.

### 2\. "http://localhost:5000/junctions" [POST] To insert a junction data

### 3\. "http://localhost:5000/get-timer" [GET] To get current values of green time of lights.

<br><br>
Thanks
