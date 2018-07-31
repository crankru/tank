# uwsgi --ini uwsgi.ini
uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file run.py --callable app