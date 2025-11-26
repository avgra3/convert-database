default:
	@echo "Simple Makefile to setup and run checks locally."
check:
	uv run --only-dev ruff check --fix .
format: check
	uv run --only-dev ruff format
