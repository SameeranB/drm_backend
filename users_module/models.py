from datetime import date

from allauth.account.models import EmailAddress
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
#
# Uncomment and edit the following User model and the Custom UserManager to represent your needs. The following has
# been coded to use Email instead of username, feel free to modify it for any particular use-case you need it for.
# You must also uncomment a line in the settings.py file that sets this model as the Auth User Model

def user_directory_path(instance, filename):
    return f"patient_information/{instance.user.email}/{filename}"


class MasterBaseClass(models.Model):

    def is_owner(self, user):
        return self.user.email == user.email

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if user.is_superuser:
            EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)

    phone = PhoneNumberField(blank=True)

    contacted = models.BooleanField(default=False)
    personal_info_complete = models.BooleanField(default=False)
    family_medical_history_complete = models.BooleanField(default=False)
    personal_medical_history_complete = models.BooleanField(default=False)
    daily_routine_complete = models.BooleanField(default=False)

    payment_method = models.CharField(max_length=50, choices=(
        ('PayTM', 'Paytm'),
        ('GPay', 'GPay'),
        ('Bank Transfer', 'Bank Transfer'),
    ), blank=True)
    payment_complete = models.BooleanField(default=False)
    on_boarding_complete = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def is_owner(self, user):
        return self.email == user.email


class PersonalInformation(MasterBaseClass):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_information')
    profile_picture = models.ImageField(blank=True, upload_to=user_directory_path, name='profile_picture')
    date_of_birth = models.DateField(blank=True)
    gender = models.CharField(max_length=50, choices=(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Rather Not Say', 'Rather Not Say'),

    ), blank=True)
    country = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)

    profession = models.CharField(max_length=100, choices=(('Retired', 'Retired'),
                                                           ('Homemaker', 'Homemaker'),
                                                           ('Service', 'Service'),
                                                           ('Self-employed', 'Self-employed')
                                                           ), blank=True)

    drive_behind_joining = models.CharField(max_length=500, blank=True)

    diet_preference = models.CharField(max_length=15, choices=(
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
        ('Eggiterian', 'Eggiterian'),
        ('Vegan', 'Vegan')
    ), blank=True)
    referral_source = models.CharField(max_length=20, choices=(
        ('Doctor', 'Doctor'),
        ('Friends', 'Friends'),
        ('Relatives', 'Relatives'),
        ('Newspapers', 'Newspapers'),
        ('Magazines', 'Magazines'),
        ('Facebook', 'Facebook'),
        ('Our Website', 'Our Website')
    ), blank=True)
    ref_name = models.CharField(max_length=50, blank=True)
    ref_number = PhoneNumberField(blank=True)
    ref_email = models.EmailField(blank=True)

    @property
    def age(self):
        if self.date_of_birth is None:
            return None
        else:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class FamilyMedicalHistory(MasterBaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_medical_history')
    type = models.CharField(max_length=50, choices=(
        ('Obesity', 'Obesity'),
        ('Blood Pressure', 'Blood Pressure'),
        ('Heart Attack / Bypass / Stroke', 'Heart Attack / Bypass / Stroke'),
        ('Diabetes', 'Diabetes'),
        ('Cancer', 'Cancer'),
        ('Hypothyroid', 'Hypothyroid')
    ))
    member = models.CharField(max_length=50, choices=(
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Grand Mother', 'Grand Mother'),
        ('Grand Father', 'Grand Father'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    ))


class PersonalMedicalHistory(MasterBaseClass):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_medical_history')

    obesity = models.BooleanField(default=False)
    blood_pressure = models.BooleanField(default=False)
    heart_issues = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    cancer = models.BooleanField(default=False)
    hypothyroid = models.BooleanField(default=False)
    hyperthyroid = models.BooleanField(default=False)
    pcod = models.BooleanField(default=False)
    menopausal = models.BooleanField(default=False)
    acidity = models.BooleanField(default=False)
    gout = models.BooleanField(default=False)
    other_dietary_issues = models.BooleanField(default=False)

    blood_report = models.FileField(upload_to=user_directory_path, name="blood_report")

    pregnancies = models.IntegerField(default=0)
    menstrual = models.CharField(max_length=20, choices=(
        ('Normal', 'Normal'),
        ('Disturbed', 'Disturbed'),
        ('Menopausal', 'Menopausal'),
        ('PCOD', 'PCOD'),
        ('Not Applicable', 'Not Applicable'),
    ), blank=True)

    highest_weight = models.FloatField(blank=True)
    lowest_weight = models.FloatField(blank=True)
    previous_efforts = models.TextField(blank=True)
    obesity_event = models.TextField(blank=True)
    lost_and_gained_times = models.IntegerField(blank=True)
    overweight_as_child = models.BooleanField(default=False)
    weight_gain_since = models.DateField(blank=True)
    reason_for_gain = models.TextField(blank=True)

    smoke = models.BooleanField(blank=True)
    smoke_level = models.CharField(max_length=100, choices=(
        ('Occasional', 'Occasional'),
        ('Regular', 'Regular'),
        ('Heavy', 'Heavy')
    ), blank=True)
    tobacco = models.BooleanField(blank=True)
    tobacco_level = models.CharField(max_length=100, choices=(
        ('Occasional', 'Occasional'),
        ('Regular', 'Regular'),
        ('Heavy', 'Heavy')
    ), blank=True)
    alcohol = models.BooleanField(blank=True)
    alcohol_level = models.CharField(max_length=100, choices=(
        ('Occasional', 'Occasional'),
        ('Regular', 'Regular'),
        ('Heavy', 'Heavy')
    ), blank=True)


class DailyRoutine(MasterBaseClass):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='daily_routine')

    wake_up_time = models.TimeField(blank=True)
    breakfast_time = models.TimeField(blank=True)
    mid_morning_time = models.TimeField(blank=True)
    lunch_time = models.TimeField(blank=True)
    lunch_location = models.CharField(max_length=100, blank=True, choices=(
        ('Home', 'Home'),
        ('Lunch Box', 'Lunch Box'),
        ('Office Canteen', 'Office Canteen'),
    ))

    tea_time = models.TimeField(blank=True)
    dinner_time = models.TimeField(blank=True)
    bed_time = models.TimeField(blank=True)

    office_start_time = models.TimeField(blank=True)
    office_end_time = models.TimeField(blank=True)

    exercise_routine = models.CharField(max_length=100, choices=(
        ('Regular', 'Regular'),
        ('Not Regular', 'Not Regular'),
    ))
    exercise_time = models.TimeField(blank=True)
    cardio = models.BooleanField(blank=True)
    strength_training = models.BooleanField(blank=True)
    yoga = models.BooleanField(blank=True)
    walk = models.BooleanField(blank=True)


class Medications(MasterBaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    dosage = models.IntegerField(blank=True)
    name = models.CharField(max_length=500)
