class BasePage:
    def __init__(self, page):
        self.page = page 

    def click(self, locator):
        locator.click()

    def fill(self, locator, value):
        locator.fill(value)

    def is_visible(self, locator):
        return locator.is_visible()

    def get_text(self, locator):
        return locator.inner_text()

    def get_attribute(self, locator, attribute_name):
        return locator.get_attribute(attribute_name)

    def get_input_value(self, locator):
        return locator.input_value()

