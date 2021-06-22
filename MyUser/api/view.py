from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from Authorizations.Authorization import IsSuperUser
from .UserSerializer import (
    UserSerializer, EditUserSerializer, AuthorUserSerializers, EditUserStatusSerializers, UserChangePasswordSerializer,
    SetPhoneNumberSerializer, GenerateSMSCodeSerializer, PrivateUserSerializer, PublicUserSerializer,
    PublicUserWithoutPostsSerializer
)
from .pagination import UserPageNumberPagination
from ..models import User, SMSCode


# show all obj
class PrivateUserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = PrivateUserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name')
    pagination_class = UserPageNumberPagination
    ordering = ('-id',)


class PublicAuthorListAPIView(ListAPIView):
    serializer_class = PublicUserWithoutPostsSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name')
    pagination_class = UserPageNumberPagination
    ordering = ('-id',)

    def get_queryset(self):
        authors = []
        users = User.objects.all()
        for user in users:
            if user.is_author():
                authors.append(user.id)
        return User.objects.filter(id__in=authors)


# show one obj
class PrivateUserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PrivateUserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class PublicUserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'


# destroy obj
class PrivateUserDestroyAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = PrivateUserSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)


class UserEditOwnAPIView(RetrieveUpdateAPIView):
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


class MakeUserAdmin(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = EditUserStatusSerializers
    permission_classes = (IsSuperUser,)
    authentication_classes = (TokenAuthentication,)


class UserChangePasswordAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, **kwargs):
        if 'pk' not in self.kwargs:
            return self.request.user


class SetPhoneNumberAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SetPhoneNumberSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, **kwargs):
        if 'pk' not in self.kwargs:
            return self.request.user


class SendSMSVerifyCode(CreateAPIView):
    queryset = SMSCode.objects.all()
    serializer_class = GenerateSMSCodeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
