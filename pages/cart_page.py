class CartPage:
    def __init__(self, page):
        self.page = page 

    def remove_product(self, product_name):
        cart_item = self.page.locator(".cart_item").filter(has_text = product_name)
        cart_item.get_by_role("button", name = "Remove").click()

    def product_in_cart(self, product_name):
        return self.page.locator(".cart_item").filter(has_text = product_name)

    def cart_badge(self):
        return self.page.locator(".shopping_cart_badge")