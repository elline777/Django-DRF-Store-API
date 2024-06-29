from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'seller'


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
             return True
        return request.user.role == 'customer'