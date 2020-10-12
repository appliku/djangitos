# Project Targets
build:
	make build-docker
	make migrate-python
	make manage-createsuperuser

build-docker:
	docker-compose build

run:
	docker-compose up

manage-python:
	docker-compose run --rm web python manage.py $(command)

makemigrations-python: command=makemigrations
makemigrations-python: manage-python
mm: makemigrations-python

migrate-python: command=migrate
migrate-python: manage-python

manage-createsuperuser: command=shell -c "from usermodel.models import User; User.objects.create_superuser(first_name='Admin', last_name='User', email='admin@example.com', password='adminpass') if User.objects.filter(email='admin@example.com').first() is None else None;"
manage-createsuperuser: manage-python
csu: manage-createsuperuse

lint:
	docker-compose run --rm web flake8

bash:
	docker-compose run --rm web sh