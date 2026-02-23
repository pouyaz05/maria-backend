release: python manage.py collectstatic --noinput
web: gunicorn painter_portfolio.wsgi:application --bind 0.0.0.0:$PORT --log-file -