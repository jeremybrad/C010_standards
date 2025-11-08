.PHONY: help install install-dev test lint format typecheck validate clean all ci

# Default target
help:
	@echo "C010_standards - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install all dependencies (including dev tools)"
	@echo ""
	@echo "Development:"
	@echo "  make test           Run test suite"
	@echo "  make test-cov       Run tests with coverage report"
	@echo "  make lint           Run Ruff linter"
	@echo "  make format         Format code with Ruff"
	@echo "  make typecheck      Run mypy type checker"
	@echo "  make validate       Run all Houston validators"
	@echo ""
	@echo "CI/Quality:"
	@echo "  make ci             Run all CI checks (lint, typecheck, test, validate)"
	@echo "  make all            Same as 'make ci'"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove Python cache files and test artifacts"
	@echo ""
	@echo "Examples:"
	@echo "  make install-dev    # First time setup"
	@echo "  make ci             # Before committing"
	@echo "  make test-cov       # Check test coverage"

# Installation
install:
	@echo ">>> Installing production dependencies..."
	pip install -r requirements.txt

install-dev: install
	@echo ">>> Installing development dependencies..."
	pip install -r requirements-dev.txt
	@echo ">>> Installing pre-commit hooks (optional)..."
	-pre-commit install

# Testing
test:
	@echo ">>> Running test suite..."
	pytest tests/ -v

test-cov:
	@echo ">>> Running tests with coverage..."
	pytest tests/ -v --cov=validators --cov-report=term --cov-report=html
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

# Code Quality
lint:
	@echo ">>> Running Ruff linter..."
	ruff check validators/ tests/

lint-fix:
	@echo ">>> Running Ruff linter with auto-fix..."
	ruff check --fix validators/ tests/

format:
	@echo ">>> Formatting code with Ruff..."
	ruff format validators/ tests/

format-check:
	@echo ">>> Checking code formatting..."
	ruff format --check validators/ tests/

typecheck:
	@echo ">>> Running mypy type checker..."
	mypy validators/ --check-untyped-defs

# Validation
validate:
	@echo ">>> Running all Houston validators..."
	python validators/run_all.py --pass-args --verbose

validate-features:
	@echo ">>> Validating Houston features config..."
	python validators/check_houston_features.py --verbose

validate-tools:
	@echo ">>> Validating Houston tools config..."
	python validators/check_houston_tools.py --verbose

validate-docmeta:
	@echo ">>> Validating Houston DocMeta tags..."
	python validators/check_houston_docmeta.py --verbose

# CI - Run all checks
ci: lint-fix format typecheck test validate
	@echo ""
	@echo "✅ All CI checks passed!"
	@echo ""
	@echo "Ready to commit. Run:"
	@echo "  git add ."
	@echo "  git commit -m 'your message'"
	@echo "  git push"

all: ci

# Cleanup
clean:
	@echo ">>> Cleaning up Python cache and test artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	@echo "✅ Cleanup complete"

# Bootstrap
bootstrap-ruff:
	@echo ">>> Bootstrapping Ruff config across workspace..."
	bash scripts/bootstrap_ruff.sh

# Documentation
docs:
	@echo ">>> Examples and documentation:"
	@echo "  - CONTRIBUTING.md - Contribution guidelines"
	@echo "  - examples/       - Example configurations"
	@echo "  - validators/     - Validator source code"
	@echo "  - tests/          - Test suite"

# Quick validation workflow
quick: lint-fix test-cov
	@echo ""
	@echo "✅ Quick validation complete!"
