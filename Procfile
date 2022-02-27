web: gunicorn Youtube_to_MP3_converter.wsgi --log-file -
worker: celery -A core.tasks worker -B --loglevel=info