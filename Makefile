.DEFAULT_GOAL := build
.EXPORT_ALL_VARIABLES:

PYTHONPATH=.

.PHONY: format
format:
	ruff format .
	ruff check --fix .

.PHONY: lint
lint:
	ruff check .

.PHONY: test
test:
	python manage.py check
	python manage.py test

.PHONY: build
build: lint test

.PHONY: run
run:
	python manage.py collectstatic --noinput
	python manage.py runserver

.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py migrate

.PHONY: docker-build
docker-build:
	sed 's/export //g' .envrc > .env
	python manage.py collectstatic --noinput
	docker build -t gridsight .

.PHONY: docker-run
docker-run:
	sed 's/export //g' .envrc > .env
	docker run -p 8000:8000 --network="host" --env-file .env gridsight

.PHONY: docker-login
docker-login:
	docker login ghcr.io -u jordan-dimov

.PHONY: docker-push
docker-push:
	docker tag gridsight ghcr.io/a115/gridsight:latest
	docker push ghcr.io/a115/gridsight:latest
