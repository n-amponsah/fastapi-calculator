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
-
- <img width="596" height="448" alt="Screenshot 2026-03-25 at 9 18 06 PM" src="https://github.com/user-attachments/assets/f5e25123-3982-455e-bbdc-fd3c2c38714e" />
<img width="1701" height="872" alt="Screenshot 2026-03-25 at 9 19 11 PM" src="https://github.com/user-attachments/assets/82c59c18-5063-4391-bdd4-161d020dab32" />
<img width="696" height="816" alt="Screenshot 2026-03-25 at 9 22 54 PM" src="https://github.com/user-attachments/assets/8fa27cbd-072a-4f2d-9af2-fa36aade53cc" />
