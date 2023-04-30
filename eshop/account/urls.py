from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('me/', views.current_user, name="currentUser"),
    path('me/update/', views.update_me, name="update_me"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/<str:token>/', views.reset_password, name="reset_password"),
]

