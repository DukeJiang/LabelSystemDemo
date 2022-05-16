# Label System Demo

## Project Overview
For this project I relied heavily on flask and server side rendering to do the work. I used flask for routing endpoints and serve static server rendered webpages to clients accessing the endpoints. The fronend portion is pretty simple, built with html and bootstrap. I used sqlite3 database for this demo but ideally we want to use cloud database solutions like gcloud datastore. I used bcrypt for user password encryption and SQLAlchemy for data modeling. I have included a requirements.txt file for setting up the virtual environment as well.

## How to run locally
- clone repo
- cd into root
- run: python3 main.py
- visit http://127.0.0.1:5000

## Improvement
Used sqlite3 for database which is not optimal for production. Ideally we want to migrate to cloud db such as gcloud datastore. I was trying to deploy onto gcloud app engine but later found out that app engine does not support sqlite3.
Also this demo is heavily backend focused and employs server side rendering. I went this route because of the time constraint, fast development process and the fact that we do not have a lot of dynamic contents. But we could just structure the backend to serve JSON data and render on the frontend with the data.