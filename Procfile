web: gunicorn djangito.wsgi --log-file -
release: bash release.sh
beat: celery -A djangito.celeryapp:app beat -S redbeat.RedBeatScheduler  --loglevel=DEBUG --pidfile /tmp/celerybeat.pid
worker: celery -A djangito.celeryapp:app  worker -Q default -n djangito.%%h --without-gossip --without-mingle --without-heartbeat --loglevel=INFO --max-memory-per-child=512000 --concurrency=1
