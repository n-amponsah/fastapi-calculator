import threading
import time

import pytest
import uvicorn
from playwright.sync_api import Page, expect, sync_playwright

from main import app

BASE_URL = "http://127.0.0.1:8001"


def _run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")


@pytest.fixture(scope="session", autouse=True)
def live_server():
    t = threading.Thread(target=_run_server, daemon=True)
    t.start()
    time.sleep(1.5)
    yield


@pytest.fixture()
def page():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


def calculate(page: Page, a: str, b: str, op: str):
    page.goto(BASE_URL)
    page.fill("#numA", a)
    page.fill("#numB", b)
    page.select_option("#op", op)
    page.click("#calcBtn")
    page.wait_for_timeout(400)


class TestPageLoad:
    def test_title(self, page: Page):
        page.goto(BASE_URL)
        expect(page).to_have_title("FastAPI Calculator")

    def test_heading_visible(self, page: Page):
        page.goto(BASE_URL)
        expect(page.locator("h1")).to_be_visible()

    def test_inputs_present(self, page: Page):
        page.goto(BASE_URL)
        expect(page.locator("#numA")).to_be_visible()
        expect(page.locator("#numB")).to_be_visible()
        expect(page.locator("#calcBtn")).to_be_visible()


class TestCalculations:
    def test_addition(self, page: Page):
        calculate(page, "3", "4", "add")
        expect(page.locator("#resultValue")).to_have_text("7")

    def test_subtraction(self, page: Page):
        calculate(page, "10", "3", "subtract")
        expect(page.locator("#resultValue")).to_have_text("7")

    def test_multiplication(self, page: Page):
        calculate(page, "6", "7", "multiply")
        expect(page.locator("#resultValue")).to_have_text("42")

    def test_division(self, page: Page):
        calculate(page, "15", "3", "divide")
        expect(page.locator("#resultValue")).to_have_text("5")

    def test_power(self, page: Page):
        calculate(page, "2", "8", "power")
        expect(page.locator("#resultValue")).to_have_text("256")

    def test_modulo(self, page: Page):
        calculate(page, "10", "3", "modulo")
        expect(page.locator("#resultValue")).to_have_text("1")


class TestErrorHandling:
    def test_divide_by_zero_shows_error(self, page: Page):
        calculate(page, "5", "0", "divide")
        expect(page.locator("#resultValue")).to_have_class("value error")

    def test_modulo_by_zero_shows_error(self, page: Page):
        calculate(page, "5", "0", "modulo")
        expect(page.locator("#resultValue")).to_have_class("value error")


class TestHistory:
    def test_history_appears_after_calculation(self, page: Page):
        page.goto(BASE_URL)
        calculate(page, "2", "2", "add")
        expect(page.locator("#historySection")).to_be_visible()

    def test_history_shows_correct_entry(self, page: Page):
        page.goto(BASE_URL)
        calculate(page, "5", "5", "add")
        expect(page.locator("#historyList")).to_contain_text("10")


class TestKeyboardInteraction:
    def test_enter_triggers_calculation(self, page: Page):
        page.goto(BASE_URL)
        page.fill("#numA", "8")
        page.fill("#numB", "2")
        page.select_option("#op", "divide")
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        expect(page.locator("#resultValue")).to_have_text("4")