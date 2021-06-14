from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from Post.models import Post


class IsAuthorOfThisPost(BasePermission):
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return bool(
            Post.objects.filter(slug=view.kwargs['slug']).first() and  # Post exists
            request.user.has_perm('Post.is_author') and  # Is author
            request.user == Post.objects.filter(  # Is Author of this post
                slug=view.kwargs['slug']).first().author
        )


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return bool(
            request.user.has_perm('Post.is_author')
        )


class IsAdminOrAuthorOfThisPost(BasePermission):
    def has_permission(self, request, view):
        is_author_of_this_post = IsAuthorOfThisPost().has_permission(request, view)
        is_author = IsAuthor().has_permission(request, view)

        return bool(is_author or is_author_of_this_post)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
