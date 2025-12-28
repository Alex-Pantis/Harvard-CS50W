From python:3
COPY .  /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

"""
# Base image — start from official Python 3 image
# "python:3" = latest Python 3 (currently 3.13)
# This gives us Python + pip + basic tools
FROM python:3

# Copy all files from your project folder to the container
# . = current folder on your computer
# /usr/src/app = folder inside the container
COPY . /usr/src/app

# Set the working directory inside the container
# All future commands run from here
WORKDIR /usr/src/app

# Install Django and other packages from requirements.txt
# This runs during "docker build"
RUN pip install -r requirements.txt

# Command to run when container starts
# "python3 manage.py runserver 0.0.0.0:8000"
# - python3 = run Python
# - manage.py runserver = start Django development server
# - 0.0.0.0:8000 = listen on all IPs, port 8000 (so you can access from browser)
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

"""