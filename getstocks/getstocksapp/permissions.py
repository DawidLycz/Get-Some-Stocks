from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return IsAdminUser().has_permission(request, view)
    
class IsOwnerOrGuestInWallet(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.owner == request.user:
            return True
        if request.user in obj.guests.all():
            if request.method in permissions.SAFE_METHODS:
                return True
        return False

class IsOwnerOrGuestInRecord(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.wallet.owner == request.user:
            return True
        if request.user in obj.wallet.guests.all():
            if request.method in permissions.SAFE_METHODS:
                return True
        return False
