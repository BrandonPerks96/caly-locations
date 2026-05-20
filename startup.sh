# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application server
echo "Starting the application server..."
gunicorn --bind=0.0.0.0:8000 --timeout 600 app.wsgi:application