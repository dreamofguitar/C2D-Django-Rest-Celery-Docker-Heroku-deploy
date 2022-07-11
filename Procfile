web: gunicorn C2D.wsgi — log-file -
release: python manage.py migrate
web: gunicorn C2D.wsgi — log-file -
worker1: celery -A C2D beat -l info
beat: celery -A C2D beat