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
            'author' in Profile.objects.filter(user=request.user).first().get_positions().split(' ') and
            request.user == Post.objects.filter(
                id=view.kwargs['pk']).first().author
        )


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return bool(
            Profile.objects.filter(user=request.user).first() and
            'author' in Profile.objects.filter(user=request.user).first().get_positions().split(' ')
        )


class IsAdminOrAuthorOfThisPost(BasePermission):
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_staff or bool(
            Post.objects.filter(id=view.kwargs['pk']) and request.user == Post.objects.filter(
                id=view.kwargs['pk']).first().author and Profile.objects.filter(
                user=request.user).first() and 'author' in Profile.objects.filter(
                user=request.user).first().get_positions().split(' ')
        )
