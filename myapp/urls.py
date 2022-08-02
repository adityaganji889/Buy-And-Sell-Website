"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
app_name='myapp'
urlpatterns = [
    path('',views.index,name='home'),
    path('contact/',views.contact,name='contact'),
    path('products/',views.products,name='products'),
    path('products/<int:pk>/',views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/',views.add_product,name='add_product'),
    path('products/update/<int:pk>',views.ProductUpdateView.as_view(),name='update_product'),
    path('products/delete/<int:pk>',views.ProductDelete.as_view(),name='delete_product'),
    path('products/mylistings',views.my_listings,name='mylistings'),
    path('success/',views.PaymentSuccessView.as_view(),name='success'),
    path('failed/',views.PaymentFailedView.as_view(),name='failed'),
    path('api/checkout-session/<id>',views.create_checkout_session,name='api_checkout_session')
]
