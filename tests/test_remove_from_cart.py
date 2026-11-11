from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from playwright.sync_api import expect
import pytest 

def test_remove_product_from_cart(logged_in_user):
    product_name = "Sauce Labs Backpack"

    products_page = ProductsPage(logged_in_user)
    products_page.products_page_opening_cart(product_name)

    cart_page = CartPage(logged_in_user)
    cart_page.remove_product(product_name)
    expect(cart_page.product_in_cart(product_name)).to_have_count(0)
    expect(cart_page.cart_badge()).to_have_count(0)