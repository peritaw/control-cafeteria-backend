#!/bin/bash
set -o errexit

echo "Building the project..."
pip install -r requirements.txt

echo "Make Migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput


echo "Collect Static..."
python manage.py collectstatic --noinput --clear

echo "Creating Admin User..."
python create_admin.py
