from pages.base_page import BasePage
class ProductsPage(BasePage):
    

    def add_product_to_cart(self, product_name):
        product = self.page.locator(".inventory_item").filter(has_text = product_name)
        self.click(product.get_by_role("button", name = "Add to cart"))

    def open_cart(self):
        self.click(self.page.locator(".shopping_cart_link"))

    def cart_badge(self):
        return self.page.locator(".shopping_cart_badge")

    def product_in_cart(self, product_name):
        return self.page.locator(".cart_item").filter(has_text = product_name)

    def products_page_opening_cart(self, product_name):
        self.add_product_to_cart(product_name)
        self.open_cart()
    