from django.urls import path
from .views import register, current_user, update_me

urlpatterns = [
   path('register/', register, name="register"),
   path('me/', current_user, name='me'),
   path('me/update/', update_me, name='update_me')
]
