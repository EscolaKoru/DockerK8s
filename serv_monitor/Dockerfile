# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME World

# Run script.py when the container launches
CMD ["python", "./script_ok.py"]
