#!/bin/sh
docker network create my_network
# Building the flask image
docker build -t my_flask_image .
# Start the PostgreSQL container
docker run --name my_postgres --network my_network -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres:latest
# Start the Flask container
docker run --name my_flask_app --network my_network -p 5000:5000 -d my_flask_image
# Wait for the PostgreSQL container to be ready
sleep 10


# Creating tables and importing data into the database
docker exec -it my_flask_app python create_tables.py
docker exec -it my_flask_app python import_csv.py

