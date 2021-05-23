from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView,
                                     CreateAPIView)
from rest_framework.permissions import AllowAny

from Authorizations.Authorization import IsAuthorOfThisPost, IsAuthor, IsAdminOrAuthorOfThisPost
from Post.models import Post
from APIViews.CustomRetrieveUpdateAPIView import RetrieveUpdateBlankUseDefaultAPIView
from .PostSerializer import PostSerializer, UpdatePostSerializer, CreatePostSerializer
from .pagination import PostPageNumberPagination


# show all obj
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body')
    pagination_class = PostPageNumberPagination
    ordering = ('-id',)


# show one obj
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    # authentication_classes = (TokenAuthentication,)


# update obj
class PostUpdateAPIView(RetrieveUpdateBlankUseDefaultAPIView):
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer
    permission_classes = (IsAuthorOfThisPost,)
    authentication_classes = (TokenAuthentication,)


# destroy obj
class PostDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrAuthorOfThisPost,)
    authentication_classes = (TokenAuthentication,)


# create obj
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthor,)
    authentication_classes = (TokenAuthentication,)