from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from APIViews.CustomRetrieveUpdateAPIView import RetrieveUpdateBlankUseDefaultAPIView
from .UserSerializer import UserSerializer, EditUserSerializer
from .pagination import UserPageNumberPagination
from ..models import User


# show all obj
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name')
    pagination_class = UserPageNumberPagination
    ordering = ('-id',)


# show one obj
class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


# destroy obj
class UserDestroyAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class UserEditOwnAPIView(RetrieveUpdateBlankUseDefaultAPIView):
    queryset = User.objects.all()
    serializer_class = EditUserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, **kwargs):
        if 'pk' not in self.kwargs:
            return self.request.user


class UserDestroyOwnAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, **kwargs):
        if 'pk' not in self.kwargs:
            return self.request.user
