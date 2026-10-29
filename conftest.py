from playwright.sync_api import sync_playwright, expect 
import pytest 
from pages.login_page import LoginPage

@pytest.fixture(scope= "session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless= False)
        yield browser
        browser.close()

@pytest.fixture
def browser_context(browser):
    context = browser.new_context()
    try:
        page = context.new_page()
        yield page 
    finally:
        context.close()

@pytest.fixture
def login_page(browser_context):
    page_object = LoginPage(browser_context)
    page_object.open_browser()
    return page_object

@pytest.fixture
def logged_in_user(browser_context):
    login_page = LoginPage(browser_context)
    login_page.login("standard_user", "secret_sauce")
    return browser_context
    