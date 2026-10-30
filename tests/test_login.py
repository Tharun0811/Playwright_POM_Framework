from pages.login_page import LoginPage
from playwright.sync_api import expect
import pytest 

@pytest.mark.regression
def test_login_page_title(login_page):
    expect(login_page.page).to_have_title("Swag Labs")

@pytest.mark.regression
def test_username_and_password_fields_visible(login_page):
    assert login_page.is_username_field_visible() is True
    assert login_page.is_password_field_visible() is True 

@pytest.mark.regression
def test_username_and_password_field_values(login_page):
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")

    assert login_page.username_value() == "standard_user"
    assert login_page.password_value() == "secret_sauce"

@pytest.mark.negative
@pytest.mark.parametrize("username, password, expected_error", 
                         [
                            pytest.param("", "", "Epic sadface: Username is required", id = "empty_credentilas"),
                            pytest.param("standard_user", "", "Epic sadface: Password is required", id ="missing_password"),
                            pytest.param("", "secret_sauce", "Epic sadface: Username is required", id= "missing_username"),
                            pytest.param("abc", "abc", "Epic sadface: Username and password do not match any user in this service", id = "invalid_credentials"),
                            pytest.param("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out.", id = "locked_out_user")
                         ])
    
def test_login_with_missing_and_invalid_credentials(login_page, username, password, expected_error):
    login_page.login(username, password)
    expect(login_page.page.get_by_text(expected_error)).to_be_visible()

@pytest.mark.smoke
@pytest.mark.regression
def test_login_with_valid_credentials(login_page):
    login_page.login("standard_user", "secret_sauce")
    expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
