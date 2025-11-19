all: ruff

ruff:
	uv run ruff format
	uv run ruff check --fix

check:
	uv run basedpyright .
