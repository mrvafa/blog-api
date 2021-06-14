from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
)
from rest_framework.permissions import IsAdminUser, AllowAny

from Authorizations.Authorization import IsAuthor
from Tag.models import Tag
from .TagSerializer import TagSerializer
from .pagination import TagPageNumberPagination


# show all obj
class TagListAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body')
    pagination_class = TagPageNumberPagination
    ordering = ('-id',)


# show one obj
class TagDetailAPIView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    permission_classes = (AllowAny,)


# update obj
class TagUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthor,)
    lookup_field = 'slug'
    authentication_classes = (TokenAuthentication,)


# destroy obj
class TagDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'slug'
    authentication_classes = (TokenAuthentication,)


# create obj
class TagCreateAPIView(CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthor,)
    authentication_classes = (TokenAuthentication,)
