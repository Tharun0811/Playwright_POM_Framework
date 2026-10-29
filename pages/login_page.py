class LoginPage:
    def __init__(self, page):
        self.page = page 

    def open_browser(self):
        self.page.goto("https://www.saucedemo.com/")

    def enter_username(self, username):
        self.page.get_by_placeholder("Username").fill(username)

    def enter_password(self, password):
        self.page.get_by_placeholder("Password").fill(password)

    def click_login_button(self):
        self.page.get_by_role("button", name = "Login").click()

    def login(self, username, password):

        self.open_browser()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def is_username_field_visible(self):
        return self.page.get_by_placeholder("Username").is_visible()

    def is_password_field_visible(self):
        return self.page.get_by_placeholder("Password").is_visible()

    def username_value(self):
        return self.page.get_by_placeholder("Username").input_value()

    def password_value(self):
        return self.page.get_by_placeholder("Password").input_value()

    

    