# Визначення директорій проекту
project_dir := .
package_dir := app

.PHONY: help
help: ## Відображення цієї довідки.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Форматування та перевірка коду

.PHONY: reformat
reformat: ## Переформатувати код
	@uv run ruff format $(project_dir)
	@uv run ruff check $(project_dir) --fix

.PHONY: lint
lint: reformat ## Перевірити код
	@uv run mypy $(project_dir)

##@ База даних

.PHONY: migration
migration: ## Створити міграцію бази даних
	@uv run alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_revision_id.py) \
	  --message $(message)

.PHONY: migrate
migrate: ## Застосувати міграції бази даних
	@uv run alembic upgrade head

.PHONY: app-run-db
app-run-db: ## Запустити контейнери бази даних
	@docker compose up -d --remove-orphans postgres redis

##@ Команди додатку

.PHONY: run
run: ## Запустити бота
	@uv run python -O -m $(package_dir)

.PHONY: app-build
app-build: ## Зібрати образ бота
	@docker compose build

.PHONY: app-run
app-run: ## Запустити бота в контейнері Docker
	@docker compose stop
	@docker compose up -d --remove-orphans

.PHONY: app-stop
app-stop: ## Зупинити контейнери Docker
	@docker compose stop

.PHONY: app-down
app-down: ## Зупинити контейнери Docker (down)
	@docker compose down

.PHONY: app-destroy
app-destroy: ## Знищити контейнери Docker
	@docker compose down -v --remove-orphans

.PHONY: app-logs
app-logs: ## Показати логи бота
	@docker compose logs -f bot

##@ Інше

.PHONY: name
name: ## Отримати назву пакету верхнього рівня
	@echo $(package_dir)
