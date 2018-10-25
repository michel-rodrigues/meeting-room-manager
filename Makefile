IMAGE = meeting-room-manager:latest
CONTAINER = meeting-room-manager
MANAGECMD = docker exec -it $(CONTAINER)

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build the container and project
	docker build --tag $(IMAGE) .
	docker stop $(CONTAINER) || true && docker rm $(CONTAINER) || true
	docker run -dit --name $(CONTAINER) -v $(shell pwd):/deploy -p 8000:8000 $(IMAGE) /bin/sh
	$(MANAGECMD) /bin/sh -c "python manage.py migrate"

test: ## Run tests
	$(MANAGECMD) python manage.py test

restart: ## Restart the container
	docker restart $(CONTAINER)

cmd: ## Access bash
	$(MANAGECMD) /bin/sh

up: ## Start webserver
	docker restart $(CONTAINER)
	$(MANAGECMD) /bin/sh -c "python manage.py runserver 127.0.0.1:8000"

down:
	docker stop $(CONTAINER)

remove:
	docker stop $(CONTAINER) || true && docker rm $(CONTAINER) || true
	docker rmi $(IMAGE)
