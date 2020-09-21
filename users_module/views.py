from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
# * Authentication Views:
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drm_backend.functions import mail
from drm_backend.permissions import IsOwnerOrAdmin, IsOwner, IsOwnerOrAdminReadOnly
from users_module.models import User, PersonalInformation, PersonalMedicalHistory, DailyRoutine, Medication, \
    FamilyMedicalHistory
from users_module.serializers import UserProfileSerializer, PaymentSerializer, AdminConfirmSerializer, \
    PersonalInformationSerializer, PersonalMedicalHistorySerializer, \
    DailyRoutineSerializer, UserDetailSerializer, AddOrViewMedicationSerializer, DeleteMedicationSerializer, \
    FamilyMedicalHistoryAddSerializer, FamilyMedicalHistoryDetailSerializer


# Create your views here.


class GoogleLogin(SocialLoginView):
    """
    This endpoint handles social logins and signups
    """
    adapter_class = GoogleOAuth2Adapter


# * User Views

class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    This viewset contains endpoints pertaining to the users on the platform
    """

    # * Configuration
    serializers = {
        'list': {
            "GET": UserProfileSerializer,
        },
        'retrieve': {
            "GET": UserDetailSerializer,
        },
        'payment': {
            "PATCH": PaymentSerializer,
        },
        'confirm': {
            "PATCH": AdminConfirmSerializer
        },
        'personal_information': {
            "PATCH": PersonalInformationSerializer
        },
        'family_medical_history': {
            "POST": FamilyMedicalHistoryAddSerializer,
            "PATCH": FamilyMedicalHistoryDetailSerializer,
            "DELETE": FamilyMedicalHistoryDetailSerializer,
        },
        'personal_medical_history': {
            "PATCH": PersonalMedicalHistorySerializer
        },
        'daily_routine': {
            "PATCH": DailyRoutineSerializer
        },
        'medication': {
            "PATCH": AddOrViewMedicationSerializer,
            "DELETE": DeleteMedicationSerializer
        }
    }

    permissions = {
        'list': [IsAuthenticated, IsAdminUser],
        'retrieve': [IsAuthenticated, IsOwnerOrAdminReadOnly],
        'payment': [IsAuthenticated, IsOwnerOrAdmin],
        'confirm': [IsAuthenticated, IsAdminUser],
        'personal_information': [IsAuthenticated, IsOwner],
        'family_medical_history': [IsAuthenticated, IsOwner],
        'personal_medical_history': [IsAuthenticated, IsOwner],
        'daily_routine': [IsAuthenticated, IsOwner],
        'medication': [IsAuthenticated, IsOwner],
    }

    queryset = User.objects.filter(is_staff=False, is_superuser=False, on_boarding_complete=False)

    # * Functions

    def get_serializer_class(self):
        return self.serializers.get(self.action).get(self.request.method)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action)

        if self.permission_classes is None:
            self.permission_classes = [IsAuthenticated]

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
        if user.payment_confirmation_requested:
            mail('Payment Confirmation Requested',
                 f"User {user.first_name} {user.last_name} has requested a payment confirmation. "
                 f"\nPlease check if you have received the payment and update the same in the system."
                 f"\nThe payment method was {user.payment_method}.",
                 "sameeranbandishti93@gmail.com")
        return Response({
            'message': "Payment information updated"
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
        personal_information = PersonalInformation.objects.get_or_create(user=user)[0]
        serializer = self.get_serializer_class()(personal_information, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Personal information updated"
        }, status=status.HTTP_200_OK)

    @action(methods=['post', 'patch', 'delete'], detail=True)
    def family_medical_history(self, request, *args, **kwargs):
        """
        This endpoint allows users to update their family medical history

        :permissions: IsAuthenticated, IsOwner
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        if request.method == 'POST':
            serializer = self.get_serializer_class()(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({
                'message': "Family medical history added"
            }, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer_class()(
                FamilyMedicalHistory.objects.get(user=user, id=request.data.get('id')),
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            if request.method == 'PATCH':
                serializer.save(user=user)
                return Response({
                    'message': "Family medical history updated"
                }, status=status.HTTP_200_OK)
            elif request.method == 'DELETE':
                family_medical_history = FamilyMedicalHistory.objects.get(user=user, id=serializer.data.get("id"))
                family_medical_history.delete()
                return Response({"message": "The family medical history has been deleted"}, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def personal_medical_history(self, request, *args, **kwargs):
        """
        This endpoint allows users to update their personal medical history

        :permissions: IsAuthenticated, IsOwner
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        personal_medical_history = PersonalMedicalHistory.objects.get_or_create(user=user)[0]
        serializer = self.get_serializer_class()(personal_medical_history, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({
            'message': "Personal medical history updated"
        }, status=status.HTTP_200_OK)

    @action(methods=['patch', 'delete'], detail=True)
    def medication(self, request, *args, **kwargs):
        """
        This endpoint allows users to add any medications they may be taking.

        :permissions: IsAuthenticated, IsOwner
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        if request.method == 'PATCH':
            serializer = self.get_serializer_class()(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({
                'message': "Medication updated"
            }, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)
            medication = Medication.objects.get(user=user, id=serializer.data.get("id"))
            medication.delete()
            return Response({"message": "The medication has been deleted"}, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def daily_routine(self, request, *args, **kwargs):
        """
        This endpoint allows users to update their personal medical history

        :permissions: IsAuthenticated, IsOwner
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        daily_routine = DailyRoutine.objects.get_or_create(user=user)
        serializer = self.get_serializer_class()(daily_routine, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({
            'message': "Daily routine updated"
        }, status=status.HTTP_200_OK)
