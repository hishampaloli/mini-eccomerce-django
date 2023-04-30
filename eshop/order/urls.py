from django.urls import path
from . import views

urlpatterns = [
    path('order/new/', views.new_order, name="new_order"),
    path('orders/', views.get_orders, name="get_orders"),
    path('order/<str:pk>/', views.get_order, name="get_order"),
    path('my_orders/', views.get_my_orders, name="get_my_orders"),
    path('orders_under_product/<str:pk>/', views.get_orders_under_product, name="get_orders_under_product"),
    path('order/<str:pk>/process/', views.process_order, name="process_order"),
    path('order/<str:pk>/process/', views.process_order, name="process_order"),
    path('create-checkout-session/', views.create_checkout_session, name="create_checkout_session"),
    path('orders/webhook/', views.stripe_webhook, name="stripe_order"),
   
]
