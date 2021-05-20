from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from Post.models import Post
from Profile.models import Profile


class IsAuthorOfThisPost(BasePermission):
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return bool(
            Post.objects.filter(id=view.kwargs['pk']).first() and
            request.user == Post.objects.filter(
                id=view.kwargs['pk']).first().author
        )


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return bool(
            Profile.objects.filter(user=request.user).first() and
            Profile.objects.filter(user=request.user).first().position == 'au'
        )


class IsAdminOrAuthorOfThisPost(BasePermission):
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return bool(Post.objects.filter(id=view.kwargs['pk']).first() and
                    request.user.is_staff) or bool(
            request.user == Post.objects.filter(id=view.kwargs['pk']).first().author)
