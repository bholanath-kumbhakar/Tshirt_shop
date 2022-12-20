from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',views.HomeView.as_view(),name="home"),
    path('orders/',login_required(views.OrdersView.as_view()),name='orders'),
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('product/<str:slug>',views.ProductView.as_view(),name='product'),
    path('addtocart/<str:slug>/<str:size>',views.Addto_Cart.as_view(),name='addtocart'),
    path('cart/',views.CartView.as_view(), name='cart'),
    path('checkout/',login_required(views.CheckoutView.as_view()), name='checkout'),
    path('validate_payment/',views.Validate_Payment_View.as_view(),name="validate_payment")
]
