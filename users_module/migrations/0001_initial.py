# Generated by Django 3.0.7 on 2020-09-26 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import users_module.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('contacted', models.BooleanField(default=False)),
                ('personal_info_complete', models.BooleanField(default=False)),
                ('personal_medical_history_complete', models.BooleanField(default=False)),
                ('daily_routine_complete', models.BooleanField(default=False)),
                ('payment_method', models.CharField(blank=True, choices=[('PayTM', 'Paytm'), ('GPay', 'GPay'), ('Bank Transfer', 'Bank Transfer')], max_length=50)),
                ('payment_confirmation_requested', models.BooleanField(default=False)),
                ('payment_complete', models.BooleanField(default=False)),
                ('on_boarding_complete', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users_module.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PersonalMedicalHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obesity', models.BooleanField(default=False)),
                ('blood_pressure', models.BooleanField(default=False)),
                ('heart_issues', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('cancer', models.BooleanField(default=False)),
                ('hypothyroid', models.BooleanField(default=False)),
                ('hyperthyroid', models.BooleanField(default=False)),
                ('pcod', models.BooleanField(default=False)),
                ('menopausal', models.BooleanField(default=False)),
                ('acidity', models.BooleanField(default=False)),
                ('gout', models.BooleanField(default=False)),
                ('other_dietary_issues', models.BooleanField(default=False)),
                ('blood_report', models.FileField(upload_to=users_module.models.user_directory_path)),
                ('pregnancies', models.IntegerField(default=0)),
                ('menstrual', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Disturbed', 'Disturbed'), ('Menopausal', 'Menopausal'), ('PCOD', 'PCOD'), ('Not Applicable', 'Not Applicable')], max_length=20)),
                ('highest_weight', models.FloatField(blank=True)),
                ('lowest_weight', models.FloatField(blank=True)),
                ('previous_efforts', models.TextField(blank=True)),
                ('obesity_event', models.TextField(blank=True)),
                ('lost_and_gained_times', models.IntegerField(blank=True)),
                ('overweight_as_child', models.BooleanField(default=False)),
                ('weight_gain_since', models.DateField(blank=True)),
                ('reason_for_gain', models.TextField(blank=True)),
                ('smoke', models.BooleanField(blank=True)),
                ('smoke_level', models.CharField(blank=True, choices=[('Occasional', 'Occasional'), ('Regular', 'Regular'), ('Heavy', 'Heavy')], max_length=100)),
                ('tobacco', models.BooleanField(blank=True)),
                ('tobacco_level', models.CharField(blank=True, choices=[('Occasional', 'Occasional'), ('Regular', 'Regular'), ('Heavy', 'Heavy')], max_length=100)),
                ('alcohol', models.BooleanField(blank=True)),
                ('alcohol_level', models.CharField(blank=True, choices=[('Occasional', 'Occasional'), ('Regular', 'Regular'), ('Heavy', 'Heavy')], max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_medical_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to=users_module.models.user_directory_path)),
                ('date_of_birth', models.DateField(blank=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Rather Not Say', 'Rather Not Say')], max_length=50)),
                ('country', models.CharField(blank=True, max_length=150)),
                ('state', models.CharField(blank=True, max_length=150)),
                ('city', models.CharField(blank=True, max_length=150)),
                ('profession', models.CharField(blank=True, choices=[('Retired', 'Retired'), ('Homemaker', 'Homemaker'), ('Service', 'Service'), ('Self-employed', 'Self-employed')], max_length=100)),
                ('drive_behind_joining', models.CharField(blank=True, max_length=500)),
                ('diet_preference', models.CharField(blank=True, choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Eggiterian', 'Eggiterian'), ('Vegan', 'Vegan')], max_length=15)),
                ('referral_source', models.CharField(blank=True, choices=[('Doctor', 'Doctor'), ('Friends', 'Friends'), ('Relatives', 'Relatives'), ('Newspapers', 'Newspapers'), ('Magazines', 'Magazines'), ('Facebook', 'Facebook'), ('Our Website', 'Our Website')], max_length=20)),
                ('ref_name', models.CharField(blank=True, max_length=50)),
                ('ref_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('ref_email', models.EmailField(blank=True, max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_information', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage', models.IntegerField(blank=True)),
                ('name', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FamilyMedicalHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Obesity', 'Obesity'), ('Blood Pressure', 'Blood Pressure'), ('Heart Attack / Bypass / Stroke', 'Heart Attack / Bypass / Stroke'), ('Diabetes', 'Diabetes'), ('Cancer', 'Cancer'), ('Hypothyroid', 'Hypothyroid')], max_length=50)),
                ('member', models.CharField(choices=[('Mother', 'Mother'), ('Father', 'Father'), ('Brother', 'Brother'), ('Sister', 'Sister'), ('Grand Mother', 'Grand Mother'), ('Grand Father', 'Grand Father'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_medical_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DailyRoutine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wake_up_time', models.TimeField(blank=True)),
                ('breakfast_time', models.TimeField(blank=True)),
                ('mid_morning_time', models.TimeField(blank=True)),
                ('lunch_time', models.TimeField(blank=True)),
                ('lunch_location', models.CharField(blank=True, choices=[('Home', 'Home'), ('Lunch Box', 'Lunch Box'), ('Office Canteen', 'Office Canteen')], max_length=100)),
                ('tea_time', models.TimeField(blank=True)),
                ('dinner_time', models.TimeField(blank=True)),
                ('bed_time', models.TimeField(blank=True)),
                ('office_start_time', models.TimeField(blank=True)),
                ('office_end_time', models.TimeField(blank=True)),
                ('exercise_routine', models.CharField(choices=[('Regular', 'Regular'), ('Not Regular', 'Not Regular')], max_length=100)),
                ('exercise_time', models.TimeField(blank=True)),
                ('cardio', models.BooleanField(blank=True)),
                ('strength_training', models.BooleanField(blank=True)),
                ('yoga', models.BooleanField(blank=True)),
                ('walk', models.BooleanField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='daily_routine', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
