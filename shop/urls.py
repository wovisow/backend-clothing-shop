from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.sign_up),
    path('login', views.login),
    path('logout', views.logout),

    path('order', views.get_create_order),

    path('cart', views.cart_view),
    path('cart/<int:pk>', views.cart_update),

    path('products', views.products),
    path('product', views.product_add),
    path('product/<int:pk>', views.product_detail),

    path('categories', views.categories)
]

