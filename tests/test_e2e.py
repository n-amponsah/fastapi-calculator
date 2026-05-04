import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"

# -------------------------------------------------------
# Registration Tests
# -------------------------------------------------------

def test_register_valid(page: Page):
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "testuser123")
    page.fill("#email", "testuser123@example.com")
    page.fill("#password", "password123")
    page.fill("#confirm", "password123")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("successful")

def test_register_short_password(page: Page):
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "testuser")
    page.fill("#email", "testuser@example.com")
    page.fill("#password", "123")
    page.fill("#confirm", "123")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("6 characters")

def test_register_empty_fields(page: Page):
    page.goto(f"{BASE_URL}/register")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("required")

# -------------------------------------------------------
# Login Tests
# -------------------------------------------------------

def test_login_valid(page: Page):
    # Register first
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "loginuser")
    page.fill("#email", "loginuser@example.com")
    page.fill("#password", "password123")
    page.fill("#confirm", "password123")
    page.click("button")
    page.wait_for_timeout(1000)

    # Then login
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", "loginuser")
    page.fill("#password", "password123")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("successful")

def test_login_wrong_password(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", "loginuser")
    page.fill("#password", "wrongpassword")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("Invalid")

def test_login_empty_fields(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("required")

# -------------------------------------------------------
# Calculation Tests
# -------------------------------------------------------

def test_add_calculation(page: Page):
    page.goto(f"{BASE_URL}/calculations-page")
    page.fill("#numA", "10")
    page.fill("#numB", "5")
    page.select_option("#opType", "Add")
    page.click("button.btn-add")
    expect(page.locator("#message")).to_contain_text("15")

def test_divide_by_zero(page: Page):
    page.goto(f"{BASE_URL}/calculations-page")
    page.fill("#numA", "10")
    page.fill("#numB", "0")
    page.select_option("#opType", "Divide")
    page.click("button.btn-add")
    expect(page.locator("#message")).to_contain_text("zero")

def test_empty_calculation_fields(page: Page):
    page.goto(f"{BASE_URL}/calculations-page")
    page.click("button.btn-add")
    expect(page.locator("#message")).to_contain_text("both numbers")
