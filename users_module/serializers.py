from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers

# * Authentication Serializers
from users_module.models import User, FamilyMedicalHistory, PersonalInformation, PersonalMedicalHistory, DailyRoutine, \
    Medication


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            # 'custom_field': self.validated_data.get('custom_field', ''),
        }


# * User ViewSet Serializers

class UserProfileSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used to display a list of users to the admin. The only fields editable are 'payment_completed' and 'contacted'
    """

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions']
        read_only_fields = ['user_id', 'email', 'first_name', 'last_name', 'payment_method', 'phone',
                            'personal_info_complete', 'family_medical_history_complete',
                            'personal_medical_history_complete', 'daily_routine_complete', 'on_boarding_complete']


class PaymentSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the user to update the payment method of the user.
    """

    class Meta:
        model = User
        fields = ['payment_method', 'payment_confirmation_requested']


class AdminConfirmSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the admin to confirm the call and the payment
    """

    class Meta:
        model = User
        fields = ['payment_complete', 'contacted']


class PersonalInformationSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by users to input their personal information.
    """

    class Meta:
        model = PersonalInformation
        exclude = ['user', 'id']


class FamilyMedicalHistorySerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the users to input family members and any conditions they may be suffering from.
    """

    class Meta:
        model = FamilyMedicalHistory
        exclude = ['user', 'id']


class PersonalMedicalHistorySerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the users to input family members and any conditions they may be suffering from.
    """

    class Meta:
        model = PersonalMedicalHistory
        exclude = ['user', 'id']


class DailyRoutineSerializer(serializers.ModelSerializer):
    """
    This serializer is used by the user to enter their daily routine.
    """

    class Meta:
        model = DailyRoutine
        exclude = ['user', 'id']


class MedicationSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by the users to enter any medications they may be using.
    """

    class Meta:
        model = Medication
        exclude = ['user', 'id']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    This serializer is to be used by both the user and the admin to view details about a user.
    """

    personal_information = PersonalInformationSerializer(read_only=True)
    personal_medical_history = PersonalMedicalHistorySerializer(read_only=True)
    medication = MedicationSerializer(read_only=True, many=True)
    family_medical_history = FamilyMedicalHistorySerializer(read_only=True, many=True)
    daily_routine = DailyRoutineSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions']
        read_only_fields = ['user_id', 'email', 'first_name', 'last_name', 'payment_method', 'phone',
                            'personal_info_complete', 'family_medical_history_complete',
                            'personal_medical_history_complete', 'daily_routine_complete', 'on_boarding_complete']
