# Use an official Python runtime as a parent image
# FROM python:3.9-slim
# FROM httpd:2.4
FROM python:3

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /chatbot

# Install Apache2 and mod_wsgi
RUN apt-get update && apt-get install -y nginx nano

# Install dependencies
COPY requirements.txt /chatbot/requirements.txt
RUN pip install -r requirements.txt
# RUN pip install uwsgi

# Copy the current directory contents into the container at /var/www/code/
COPY chatbot /chatbot

# RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Copy nginx configuration file
COPY nginx/default.conf /etc/nginx/sites-available/default

# Copy uWSGI configuration file
COPY ./uwsgi/uwsgi.ini /etc/uwsgi/uwsgi.ini

# Expose the port
EXPOSE 8001
EXPOSE 8002

# Start uWSGI and Nginx
CMD ["sh", "-c", "uwsgi --ini /etc/uwsgi/uwsgi.ini & nginx -g 'daemon off;'"]

# Build and Run the Docker Container
# docker build -t chatbot_django_app .
# docker run -d -p 8001:80 chatbot_django_app

