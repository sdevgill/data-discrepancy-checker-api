build: ## Build the container
	docker compose build

up: ## Start container (in foreground)
	docker compose up &

down: ## Stop container
	docker compose down

test: ## Run tests
	docker compose run app pytest src

.PHONY: build up down test
