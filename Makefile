# Makefile for Python project with Docker Compose

# Variables
DOCKER_COMPOSE = docker compose
DOCKER = docker
PYTHON = python3

# Default target
.PHONY: help
help:
	@echo "Makefile commands:"

# Start services
.PHONY: api
api:
	$(DOCKER_COMPOSE) up -d --build

.PHONY: api-logs
api-logs:
	$(DOCKER) logs bix_app --tail 100 -f

.PHONY: db-logs
db-logs:
	$(DOCKER) logs bix_db --tail 100 -f

.PHONY: go-inside-app 
go-inside-app:
	$(DOCKER) exec -it bix_app sh

.PHONY: makemigrations
makemigrations:
	$(DOCKER) exec -it bix_app python manage.py makemigrations

.PHONY: migrate
migrate:
	$(DOCKER) exec -it bix_app python manage.py migrate

.PHONY: createsuperuser
createsuperuser:
	$(DOCKER) exec -it bix_app python manage.py createsuperuser

.PHONY: test
test:
	$(DOCKER) exec -it bix_app python manage.py test --debug-mode



