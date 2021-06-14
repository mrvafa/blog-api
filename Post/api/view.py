from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
)
from rest_framework.permissions import AllowAny

from Authorizations.Authorization import IsAuthorOfThisPost, IsAuthor, IsAdminOrAuthorOfThisPost
from Post.models import Post
from .PostSerializer import PostSerializer, UpdatePostSerializer, CreatePostSerializer
from .pagination import PostPageNumberPagination


# show all obj
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body')
    pagination_class = PostPageNumberPagination
    ordering = ('-id',)


# show one obj
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = (AllowAny,)


# update obj
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer
    permission_classes = (IsAuthorOfThisPost,)
    lookup_field = 'slug'
    authentication_classes = (TokenAuthentication,)


# destroy obj
class PostDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrAuthorOfThisPost,)
    lookup_field = 'slug'
    authentication_classes = (TokenAuthentication,)


# create obj
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthor,)
    authentication_classes = (TokenAuthentication,)
