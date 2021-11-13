web: gunicorn project.wsgi --log-file -
release: bash release.sh
beat: celery -A project.celeryapp:app beat -S redbeat.RedBeatScheduler  --loglevel=DEBUG --pidfile /tmp/celerybeat.pid
worker: celery -A project.celeryapp:app  worker -Q default -n project.%%h --without-gossip --without-mingle --without-heartbeat --loglevel=INFO --max-memory-per-child=512000 --concurrency=1
