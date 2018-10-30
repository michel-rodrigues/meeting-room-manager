IMAGE = meeting-room-manager:latest
CONTAINER = meeting-room-manager
MANAGECMD = docker exec -it $(CONTAINER)

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build the container and project
	docker build --tag $(IMAGE) .
	docker stop $(CONTAINER) || true && docker rm $(CONTAINER) || true
	docker run -dit --name $(CONTAINER) -v $(shell pwd):/deploy -p 8000:8000 $(IMAGE) /bin/sh
	$(MANAGECMD) /bin/sh -c "python manage.py migrate"

run: ## Run container
	docker run -dit --name $(CONTAINER) -v $(shell pwd):/deploy -p 8000:8000 $(IMAGE) /bin/sh

test: ## Run tests
	$(MANAGECMD) python manage.py test

coverage: ## Run tests over coverage and show report
	$(MANAGECMD) coverage run manage.py test
	$(MANAGECMD) coverage report

report: ## Generate HTML report
	$(MANAGECMD) coverage html
	xdg-open htmlcov/index.html

restart: ## Restart container
	docker restart $(CONTAINER)

cmd: ## Access container bash
	$(MANAGECMD) /bin/sh

up: ## Start container and webserver
	docker restart $(CONTAINER)
	$(MANAGECMD) /bin/sh -c "python manage.py runserver 0.0.0.0:8000"

down: ## Stop container
	docker stop $(CONTAINER)

remove: ## Remove container and image
	docker stop $(CONTAINER) || true && docker rm $(CONTAINER) || true
	docker rmi $(IMAGE)
