from django import template
from totembo.models import Category, Favourites
from totembo.utils import get_cart_data

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_normal_price(price):
    return f"{price:_}".replace("_", " ")

@register.simple_tag()
def check_favourites(user):
    fav_products = Favourites.objects.filter(user=user)
    products = [i.product for i in fav_products]
    return products

@register.simple_tag()
def check_cart(request):
    products = get_cart_data(request)['order_products']
    cart_products = [i.product for i in products]

    return cart_products





