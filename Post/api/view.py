from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView,
                                     CreateAPIView)
from rest_framework.permissions import IsAdminUser, AllowAny

from Post.models import Post
from .PostSerializer import PostSerializer, UpdatePostSerializer
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
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


# destroy obj
class PostDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


# create obj
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)
