import pytest
from playwright.sync_api import Page, expect, sync_playwright

BASE_URL = "http://localhost:8000"

# -------------------------------------------------------
# Registration Tests
# -------------------------------------------------------

def test_register_valid(page: Page):
    """Positive: Register with valid data"""
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "testuser123")
    page.fill("#email", "testuser123@example.com")
    page.fill("#password", "password123")
    page.fill("#confirm", "password123")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("successful")

def test_register_short_password(page: Page):
    """Negative: Register with short password"""
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "testuser")
    page.fill("#email", "testuser@example.com")
    page.fill("#password", "123")
    page.fill("#confirm", "123")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("6 characters")

def test_register_password_mismatch(page: Page):
    """Negative: Passwords don't match"""
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "testuser")
    page.fill("#email", "testuser@example.com")
    page.fill("#password", "password123")
    page.fill("#confirm", "different123")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("do not match")

def test_register_empty_fields(page: Page):
    """Negative: Empty fields"""
    page.goto(f"{BASE_URL}/register")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("required")

# -------------------------------------------------------
# Login Tests
# -------------------------------------------------------

def test_login_valid(page: Page):
    """Positive: Login with valid credentials"""
    # First register the user
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", "loginuser")
    page.fill("#email", "loginuser@example.com")
    page.fill("#password", "password123")
    page.fill("#confirm", "password123")
    page.click("button")
    page.wait_for_timeout(1000)

    # Now login
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", "loginuser")
    page.fill("#password", "password123")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("successful")

def test_login_wrong_password(page: Page):
    """Negative: Wrong password shows error"""
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", "loginuser")
    page.fill("#password", "wrongpassword")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("Invalid credentials")

def test_login_empty_fields(page: Page):
    """Negative: Empty fields"""
    page.goto(f"{BASE_URL}/login")
    page.click("button")
    expect(page.locator("#message")).to_contain_text("required")
