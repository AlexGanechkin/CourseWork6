from rest_framework.permissions import BasePermission

from users.managers import UserRoles


class IsCurrentUser(BasePermission):

    #def has_permission(self, request, view):
    #    return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        #return request.user.pk == obj.author.pk
        return obj.author == request.user


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == UserRoles.ADMIN:
            return True
        return False
