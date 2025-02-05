from .models import Product, OrderProducts, Order, Customer

class Cart:
    def __init__(self, request, product_slug=None, action=None):
        self.request = request

        if product_slug and action:
            self.add_or_delete(product_slug, action)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        order, created = Order.objects.get_or_create(customer=customer)

        order_products = order.ordered_products.all()

        context = {
            'order': order,
            'order_products': order_products
        }

        return context

    def add_or_delete(self, product_slug, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(slug=product_slug)

        order_product, created = OrderProducts.objects.get_or_create(product=product, order=order)

        if action == 'add' and product.quantity > 0 and product.quantity > order_product.quantity:
            order_product.quantity += 1
            order_product.save()

        elif action == 'delete':
            order_product.quantity -= 1
            order_product.save()

        elif action == 'delete_product':
            order_product.delete()



        if order_product.quantity <= 0:
            order_product.delete()


    def clear_cart_after_payment(self):
        order = self.get_cart_info()['order']
        order_products = order.ordered_products.all()

        for product in order_products:
            item = Product.objects.get(pk=product.product.pk)
            item.quantity -= 1
            item.save()

        order.delete()



def get_cart_data(request):
    cart = Cart(request)
    cart_info = cart.get_cart_info()

    return cart_info






