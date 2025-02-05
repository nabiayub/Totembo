from django.contrib.auth import login, logout
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .tests import get_next_page, change_sum_to_dollar
from .utils import Cart, get_cart_data
import stripe
from shop import settings


# Create your views here.


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'totembo/index.html'
    extra_context = {
        'title': 'Totembo - магазин аксессуаров'
    }

    def get_queryset(self):
        categories = Category.objects.all()
        products = []
        for category in categories:
            product = Product.objects.filter(category=category)[::-1][:2]
            products += product

        return products


class ProductListByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'totembo/category_detail.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Category.objects.get(slug=self.kwargs['slug']).title

        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'totembo/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        reviews = Reviews.objects.filter(product=product)
        context['title'] = product.title
        context['products'] = Product.objects.all()[::-1][:4]
        context['form'] = ReviewForm()
        context['reviews'] = reviews

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                review = form.save(commit=False)

                review.user = request.user
                review.product = self.object
                review.save()
                return redirect('product_detail', self.object.slug)
            return self.get(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)


def save_to_favourites(request, slug):
    if request.user.is_authenticated:
        product = Product.objects.get(slug=slug)

        new_product, action = Favourites.objects.get_or_create(user=request.user, product=product)
        new_product.save()

        if action == False:
            new_product.delete()

        next_page = get_next_page(request)
        return redirect(next_page)
    else:
        return redirect('login')


class FavouriteListView(LoginRequiredMixin, ListView):
    model = Favourites
    context_object_name = 'products'
    template_name = 'totembo/favourites.html'
    extra_context = {
        'title': 'Избранное'
    }
    login_url = 'login'

    def get_queryset(self):
        all_products = Favourites.objects.filter(user=self.request.user)
        products = [i.product for i in all_products]

        return products


def clear_favourites(request):
    if request.user.is_authenticated:
        products = Favourites.objects.filter(user=request.user)
        products.delete()
        return redirect('favourites')
    else:
        return redirect('login')


def delete_review(request, pk):
    if request.user.is_authenticated:
        review = Reviews.objects.get(pk=pk)
        if request.user == review.user:
            review.delete()
        return redirect('product_detail', review.product.slug)

    else:
        return redirect('lofin')


class ReviewChangeView(UpdateView):
    model = Reviews
    form_class = ReviewForm
    template_name = 'totembo/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        review = Reviews.objects.get(pk=self.kwargs['pk'])
        review.updated = True
        review.save()

        product = Product.objects.get(pk=review.product.pk)
        products = Product.objects.all()[::-1][:4]
        all_reviews = Reviews.objects.filter(product=review.product)
        reviews = [i for i in all_reviews if i.pk != review.pk]

        context['product'] = product
        context['title'] = 'Изменить комметарий'
        context['products'] = products
        context['reviews'] = reviews

        return context

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.object.product.slug})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            review = Reviews.objects.get(pk=self.kwargs['pk'])
            if review.user == request.user:
                return super(ReviewChangeView, self).get(request, *args, **kwargs)
        return redirect('main')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')
                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            form = LoginForm()

        context = {
            'title': 'Вход в акааунт',
            'form': form
        }

        return render(request, 'totembo/login.html', context)
    else:
        return redirect('main')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegistrationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                phone = request.POST.get('phone')
                profile = Profile.objects.create(user=user, phone=phone)
                profile.save()
                return redirect('login')
            else:
                return redirect('registration')

        else:
            form = RegistrationForm()

        context = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request, 'totembo/registration.html', context)
    else:
        return redirect('login')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form1 = EditAccountForm(data=request.POST, instance=request.user)
            form2 = EditProfileForm(data=request.POST, instance=request.user.profile)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                return redirect('profile')
            else:
                return redirect('profile')
        else:
            account_form = EditAccountForm(instance=request.user)
            profile_form = EditProfileForm(instance=request.user.profile)

        profile = Profile.objects.get(user=request.user)
        if profile:
            try:
                customer = Customer.objects.get(user=request.user)
                saved_order = SaveOrder.objects.filter(customer=customer)
            except:
                saved_order = []

            context = {
                'form1': account_form,
                'form2': profile_form,
                'title': 'Профиль',
                'orders': saved_order[::-1][:1]
            }
        else:
            return redirect('login')

        return render(request, 'totembo/profile.html', context)


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Ваша корзина',
            'order': cart_info['order'],
            'order_products': cart_info['order_products']
        }

        return render(request, 'totembo/cart.html', context)


def add_to_cart(request, product_slug, action):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_cart = Cart(request, product_slug, action)

        next_page = get_next_page(request)
        return redirect(next_page)


def clear_cart(request):
    if request.user.is_authenticated:
        order = get_cart_data(request)['order']
        order.delete()
        return redirect('cart')

    else:
        return redirect('login')


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart_info = get_cart_data(request)
        customer = Customer.objects.get(pk=cart_info['order'].customer.pk)

        context = {
            'order': cart_info['order'],
            'order_products': cart_info['order_products'],

            'customer_form': CustomerForm(instance=customer),
            'shipping_form': ShippingForm(),
            'title': 'Оформление заказа'
        }

        return render(request, 'totembo/checkout.html', context)


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.method == 'POST':
            user_cart = Cart(request)
            cart_info = get_cart_data(request)

            customer_form = CustomerForm(data=request.POST)
            shipping_form = ShippingForm(data=request.POST)

            if customer_form.is_valid() and shipping_form.is_valid():
                customer = Customer.objects.get(user=request.user)
                customer.first_name = customer_form.cleaned_data['first_name']
                customer.last_name = customer_form.cleaned_data['last_name']
                customer.telegram = customer_form.cleaned_data['telegram']
                customer.save()

                shipping = shipping_form.save(commit=False)
                shipping.customer = customer
                shipping.order = cart_info['order']
                shipping.save()
            else:
                return redirect('checkout')

            total_price = cart_info['order'].get_cart_total_price
            total_price_in_dollars = change_sum_to_dollar(total_price)
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Товары LOFT'},
                        'unit_amount': int(total_price_in_dollars)
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('checkout'))
            )

            return redirect(session.url, 303)

        else:
            return redirect('checkout')


def success_payment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_cart = Cart(request)
        cart_info = get_cart_data(request)
        order = cart_info['order']

        save_order = SaveOrder.objects.create(customer=order.customer,
                                              order_number=order.pk,
                                              total_price=order.get_cart_total_price,
                                              completed=True)
        save_order.save()

        for item in order.ordered_products.all():
            save_products = SaveOrderProduct.objects.create(
                order_id=save_order.pk,
                product=str(item),
                quantity=item.quantity,
                final_price=item.get_product_price_with_discount,
                product_price=item.product.price,
                photo=item.product.get_product_first_photo(),
                color_name=item.product.color_name
            )

            save_products.save()

        user_cart.clear_cart_after_payment()

        context = {
            'title': 'Статус оплаты'
        }

        return render(request, 'totembo/success.html', context)


class History(LoginRequiredMixin, ListView):
    model = SaveOrder
    context_object_name = 'orders'
    template_name = 'totembo/history.html'
    extra_context = {
        'title': 'История заказов'
    }
    login_url = 'login'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        saved_order = SaveOrder.objects.filter(customer=customer)

        return saved_order

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=self.request.user)
        saved_order = SaveOrder.objects.filter(customer=customer)

        if saved_order:
            return super(History, self).get(request, *args, **kwargs)
        else:
            return redirect('profile')

