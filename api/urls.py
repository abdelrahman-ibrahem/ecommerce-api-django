from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register),
    path('products/', views.ListCreateProduct.as_view()),
    path('order/create/', views.create_order),
    path('orders/', views.ListOrder.as_view()),
    path('add-to-cart/', views.add_to_cart),
    path('my-cart/', views.MyCart.as_view())

]
