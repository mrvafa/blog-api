from rest_framework.permissions import BasePermission

from Post.models import Post
from Profile.models import Profile


class IsAuthorOfThisPost(BasePermission):
    def has_permission(self, request, view):
        if not Post.objects.filter(id=view.kwargs['pk']).first():
            return False
        return bool(
            request.user and request.user == Post.objects.filter(
                id=view.kwargs['pk']).first().author
        )


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if not Profile.objects.filter(user=request.user).first():
            return False
        return bool(
            request.user and
            Profile.objects.filter(user=request.user).first().position == 'au'
        )


class IsAdminOrAuthorOfThisPost(BasePermission):
    def has_permission(self, request, view):
        if not Post.objects.filter(id=view.kwargs['pk']).first():
            return False
        return bool(request.user and request.user.is_staff) or bool(
            request.user and request.user == Post.objects.filter(id=view.kwargs['pk']).first().author)
