#!/bin/bash

echo "Building Django app for Vercel..."

# Install dependencies using pip (not uv)
pip install --upgrade pip
pip install -r requirements.txt

# Run Django collectstatic
python manage.py collectstatic --noinput

echo "Build completed!"