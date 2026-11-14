from pages.base_page import BasePage
class LoginPage(BasePage):
     

    def open_browser(self):
        self.page.goto("https://www.saucedemo.com/")

    def enter_username(self, username):
        self.fill(self.page.get_by_placeholder("Username"), username)

    def enter_password(self, password):
        self.fill(self.page.get_by_placeholder("Password"), password)

    def click_login_button(self):
        self.click(self.page.get_by_role("button", name = "Login"))

    def login(self, username, password):

        self.open_browser()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def is_username_field_visible(self):
        return self.is_visible(self.page.get_by_placeholder("Username"))

    def is_password_field_visible(self):
        return self.is_visible(self.page.get_by_placeholder("Password"))

    def username_value(self):
        return self.get_input_value(self.page.get_by_placeholder("Username"))

    def password_value(self):
        return self.get_input_value(self.page.get_by_placeholder("Password"))

    def get_error_message(self):
        return self.get_text(self.page.locator("[data-test='error']"))

    def get_username_placeholder(self):
        return self.get_attribute(
        self.page.get_by_placeholder("Username"),
        "placeholder"
    )
    

    