class ProductsPage:
    def __init__(self, page):
        self.page = page 

    def add_product_to_cart(self, product_name):
        product = self.page.locator(".inventory_item").filter(has_text = product_name)
        product.get_by_role("button", name = "Add to cart").click()

    def open_cart(self):
        self.page.locator(".shopping_cart_link").click()

    def cart_badge(self):
        return self.page.locator(".shopping_cart_badge")

    def product_in_cart(self, product_name):
        return self.page.locator(".cart_item").filter(has_text = product_name)
    