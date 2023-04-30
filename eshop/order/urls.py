from django.urls import path
from . import views

urlpatterns = [
    path('order/new/', views.new_order, name="new_order"),
    path('orders/', views.get_orders, name="get_orders"),
    path('order/<str:pk>/', views.get_order, name="get_order"),
    path('order/<str:pk>/process/', views.process_order, name="process_order"),
    path('order/<str:pk>/process/', views.process_order, name="process_order"),
    path('create-checkout-session/', views.create_checkout_session, name="create_checkout_session"),
    path('orders/webhook/', views.stripe_webhook, name="stripe_order"),
    
]
