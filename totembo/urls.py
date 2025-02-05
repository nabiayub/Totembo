from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='main'),
    path('category/<slug:slug>/', ProductListByCategory.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('save_to_favourites/<slug:slug>/', save_to_favourites, name='save_to_favourites'),
    path('favourites/', FavouriteListView.as_view(), name='favourites'),
    path('clear_favourites/', clear_favourites, name='clear_favourites'),
    path('delete_review/<int:pk>', delete_review, name='delete_review'),
    path('change_review/<int:pk>', ReviewChangeView.as_view(), name='change_review'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', registration, name='registration'),
    path('profile/', profile_view, name='profile'),
    path('cart/', cart_view, name='cart'),
    path('to_cart/<slug:product_slug>/<str:action>', add_to_cart, name='add_to_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('checkout', checkout_view, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
    path('history/', History.as_view(), name='history')
]