from pages.products_page import ProductsPage
import pytest 
from playwright.sync_api import expect

@pytest.mark.smoke
@pytest.mark.regression
def test_add_product_to_shopping_cart(logged_in_user):
    product_name = "Sauce Labs Backpack"
    products_page = ProductsPage(logged_in_user)
    products_page.add_product_to_cart(product_name)
    expect(products_page.cart_badge()).to_have_text("1")
    products_page.open_cart()
    expect(products_page.product_in_cart(product_name)).to_be_visible()