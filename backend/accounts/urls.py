from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-phone-register/', views.verify_phone_register, name='verify_phone_register'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('profile/', views.profile_view, name='profile'),
    
    # Email verification and password reset URLs
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Social Auth URLs
    path('social-auth/', include('social_django.urls', namespace='social')),
] 