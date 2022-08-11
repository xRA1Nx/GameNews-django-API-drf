from rest_framework import permissions
from gamenews_app.models import Author


# Права на чтение всем, права на редактирование - только собстенникам ресурса
class IsPostOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.user.id == request.user.id


class IsCategoryPostOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.post.author.user.id == request.user.id


# Права на чтение всем, права на редактирование - только админам
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return all([request.user, request.user.is_staff])


# Права на чтение всем, права на редактирование - только админам
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        author = Author.objects.filter(user=request.user.id)
        if author:
            return all([request.user, author.exists(), author[0].is_active])
        else:
            return False

