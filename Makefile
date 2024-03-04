help:
	@echo 'Makefile for managing web application                              '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo ' make up               creates containers and starts service       '
	@echo ' make down             stops service and removes containers        '
	@echo '                                                                   '
	@echo ' make migrate          run all migration                           '

up:
	docker compose -f docker-compose.yaml up -d --build

down:
	docker compose -f docker-compose.yaml down

migrate:
	docker compose exec app alembic upgrade head

view-docs:
	open http://localhost:8000/docs/