# FastAPI Calculator

A calculator web application built with FastAPI, complete with unit tests, integration tests, end-to-end Playwright tests, logging, and GitHub Actions CI.

## Operations
- Addition, Subtraction, Multiplication, Division, Power, Modulo

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python3 main.py
```

Open http://localhost:8000 in your browser.

## Running Tests
```bash
pytest tests/ -v
```

## Project Structure

- `main.py` - FastAPI app and web UI
- `operations.py` - Math functions with logging
- `tests/test_unit.py` - Unit tests
- `tests/test_integration.py` - Integration tests
- `tests/test_e2e.py` - End-to-end Playwright tests
- `.github/workflows/ci.yml` - GitHub Actions CI