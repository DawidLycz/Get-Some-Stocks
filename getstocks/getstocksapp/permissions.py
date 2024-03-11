from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return IsAdminUser().has_permission(request, view)