from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class ManagerAuthentication(BasePermission):
    message = 'Only admin users with email admin@gmail.com are allowed.'

    def has_permission(self, request, view):
        user = request.user

        if user.email == 'hisham@gmail.com':
            return True
        else:
            return False