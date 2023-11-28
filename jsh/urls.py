from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('about/', views.about_us, name='about_us'), 
    path('contact/', views.contact_us, name='contact_us'),
    path('login/', views.user_login, name='login'),  
    path('register/', views.registration, name='registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('add_to_cart/<int:item_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/cart_item_count/', views.cart_item_count, name='cart_item_count'),
    path('category/<str:category>/', views.category_items_view, name='category_items'),
    path('add_to_wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist'), 
    path('api/wishlist_item_count/', views.wishlist_item_count, name='wishlist_item_count'),
]
