default:
	@echo "Simple Makefile to setup and run checks locally."
check:
	uv run --only-dev ruff check --fix .
format:
	uv run --only-dev ruff format
type: format
	uv run --only-dev ty check
test: type
	uv run --only-dev pytest -vvv
