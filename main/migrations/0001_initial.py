# Generated by Django 4.2.5 on 2023-12-18 06:10

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(default=uuid.uuid4, max_length=15, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_child', models.BooleanField(default=False)),
                ('is_caregiver', models.BooleanField(default=False)),
                ('is_driver', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', main.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CaregiverProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.TextField(default='')),
                ('last_name', models.TextField(default='')),
                ('address', models.TextField()),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField(null=True)),
                ('nik', models.CharField(max_length=20)),
                ('npwp', models.CharField(max_length=20)),
                ('bank_name', models.CharField(max_length=100)),
                ('bank_account_number', models.CharField(max_length=30)),
                ('certificate_count', models.IntegerField(default=0)),
                ('certificate1_name', models.CharField(max_length=100)),
                ('certificate1_number', models.CharField(max_length=50)),
                ('certificate1_year', models.IntegerField(null=True)),
                ('certificate1_organizer', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ChildProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.TextField(default='')),
                ('last_name', models.TextField(default='')),
                ('address', models.TextField()),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField(null=True)),
                ('father_name', models.CharField(max_length=100)),
                ('father_occupation', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('mother_occupation', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DriverProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.TextField(default='')),
                ('last_name', models.TextField(default='')),
                ('address', models.TextField()),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField(null=True)),
                ('nik', models.CharField(max_length=20)),
                ('npwp', models.CharField(max_length=20)),
                ('bank_name', models.CharField(max_length=100)),
                ('bank_account_number', models.CharField(max_length=30)),
                ('driver_license_number', models.CharField(max_length=50)),
                ('available_working_days', models.CharField(max_length=10)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
    ]
