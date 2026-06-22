#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Building Django app..."

# Install dependencies using pip
pip install --upgrade pip
pip install -r requirements.txt

# Run Django collectstatic
python manage.py collectstatic --noinput

# Run Django database migrations
python manage.py migrate --noinput

echo "Build completed!"