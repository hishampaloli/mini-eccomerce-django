from django.urls import path
from . import views

urlpatterns = [
    path('my_cart/', views.my_cart, name="my_cart"),
    path('clear_cart/', views.clear_cart, name="clear_cart"),
    path('add_to_cart/<str:pk>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<str:pk>/', views.remove_from_cart, name="remove_from_cart"),
    
]
