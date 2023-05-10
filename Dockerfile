# Use the official Python base image
FROM python:3.9-slim

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

ENV DATABASE_URL=postgresql://myuser:mypassword@my_postgres:5432/mydb

# Make port 5000 available to the world outside this container
EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["run.py" ]

