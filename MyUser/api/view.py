from django.contrib.auth.models import Permission
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from APIViews.CustomRetrieveUpdateAPIView import RetrieveUpdateBlankUseDefaultAPIView
from Authorizations.Authorization import IsSuperUser
from .UserSerializer import (UserSerializer, EditUserSerializer, AuthorUserSerializers,
                             EditUserStatusSerializers)
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


class UserAuthor(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorUserSerializers
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def put(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        if 'is_author' in request.data:
            permission = Permission.objects.get(codename='add_post')
            if request.data['is_author'] == 'true':
                user.user_permissions.add(permission)
            else:
                user.user_permissions.remove(permission)
        return super(UserAuthor, self).put(request, args, kwargs)


class MakeUserAdmin(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = EditUserStatusSerializers
    permission_classes = (IsSuperUser,)
    authentication_classes = (TokenAuthentication,)

    def put(self, request, *args, **kwargs):
        user = User.objects.filter(id=kwargs['pk']).first()
        permission = Permission.objects.filter(codename='add_post').first()
        user.user_permissions.add(permission)
        return super(MakeUserAdmin, self).put(request, args, kwargs)
