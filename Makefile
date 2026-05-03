.PHONY: install up down rebuild worker run

install:
	uv sync

up:
	docker compose up -d

down:
	docker compose down

rebuild:
	docker compose down && docker compose up -d --build

worker:
	uv run python cmd/worker.py

run:
	uv run python hello.py
