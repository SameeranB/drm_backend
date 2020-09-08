from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
# * Authentication Views:
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drm_backend.functions import mail
from drm_backend.permissions import IsOwnerOrAdmin, IsOwner
from users_module.models import User, PersonalInformation
from users_module.serializers import UserProfileSerializer, PaymentSerializer, AdminConfirmSerializer


# Create your views here.


class GoogleLogin(SocialLoginView):
    """
    This endpoint handles social logins and signups
    """
    adapter_class = GoogleOAuth2Adapter


# * User Views

class UserViewSet(ListModelMixin, GenericViewSet):
    """
    This viewset contains endpoints pertaining to the users on the platform
    """

    # * Configuration
    serializers = {
        'list': UserProfileSerializer,
        'payment': PaymentSerializer,
        'confirm': AdminConfirmSerializer
    }

    permissions = {
        'list': [IsAuthenticated, IsAdminUser],
        'payment': [IsAuthenticated, IsOwnerOrAdmin],
        'confirm': [IsAuthenticated, IsAdminUser],
        'personal_information': [IsAuthenticated, IsOwner],
        'family_medical_history': [IsAuthenticated, IsOwner],
        'personal_medical_history': [IsAuthenticated, IsOwner],
        'daily_routine': [IsAuthenticated, IsOwner],
    }

    queryset = User.objects.filter(is_staff=False, is_superuser=False, on_boarding_complete=False)

    # * Functions

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action)
        return super(UserViewSet, self).get_permissions()

    # * Endpoints

    @action(methods=['patch'], detail=True)
    def payment(self, request, *args, **kwargs):
        """
        This endpoint is to be used by the user to select a payment method and request confirmation from the admin side.

        :permissions: IsAuthenticated, IsOwnerOrAdmin
        :param request: payment_method
        :param kwargs: user_id
        :return: 200
        """
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        mail('Payment Confirmation Requested',
             f"User {user.first_name} {user.last_name} has requested a payment confirmation. "
             f"\nPlease check if you have received the payment and update the same in the system."
             f"\nThe payment method was {user.payment_method}.",
             "sameeranbandishti93@gmail.com")
        return Response({
            'message': "Payment method updated"
        }, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def confirm(self, request, *args, **kwargs):
        """
        This endpoint is to be used by admins to confirm payment and confirm the initial call

        :permissions: IsAuthenticated, IsAdminUser
        :param request: contacted, payment_complete
        :param kwargs: user_id
        :return: 200
        """
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "User information updated"
        }, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def personal_information(self, request, *args, **kwargs):
        """
        This endpoint allows users to update their personal information

        :permissions: IsAuthenticated, IsOwner
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        personal_information = PersonalInformation.objects.get_or_create(user=user)
        serializer = self.get_serializer_class()(personal_information, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Personal information updated"
        }, status=status.HTTP_200_OK)

    # Todo: Family medical history should be multiple. Medications should be nested.
