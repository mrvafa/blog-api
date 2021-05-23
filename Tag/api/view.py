from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView,
                                     CreateAPIView)
from rest_framework.permissions import IsAdminUser, AllowAny

from APIViews.CustomRetrieveUpdateAPIView import RetrieveUpdateBlankUseDefaultAPIView
from Authorizations.Authorization import IsAuthor
from Tag.models import Tag
from .TagSerializer import TagSerializer, UpdateTagSerializer, RemoveTagImageSerializer
from .pagination import TagPageNumberPagination


# show all obj
class TagListAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body')
    pagination_class = TagPageNumberPagination
    ordering = ('-id',)


# show one obj
class TagDetailAPIView(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    # authentication_classes = (TokenAuthentication,)


# update obj
class TagUpdateAPIView(RetrieveUpdateBlankUseDefaultAPIView):
    queryset = Tag.objects.all()
    serializer_class = UpdateTagSerializer
    permission_classes = (IsAuthor,)
    authentication_classes = (TokenAuthentication,)


# destroy obj
class TagDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


# create obj
class TagCreateAPIView(CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthor,)
    authentication_classes = (TokenAuthentication,)


class TagRemoveImage(RetrieveUpdateBlankUseDefaultAPIView):
    queryset = Tag.objects.all()
    serializer_class = RemoveTagImageSerializer
    permission_classes = (IsAuthor,)
    authentication_classes = (TokenAuthentication,)