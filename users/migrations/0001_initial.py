# Generated by Django 3.0.8 on 2020-08-03 20:08

from django.db import migrations, models
import django.utils.timezone
import users.models.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(error_messages={'unique': 'Email already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('birthday', models.CharField(max_length=12, verbose_name='Birthday')),
                ('phone', models.CharField(max_length=10, verbose_name='Phone')),
                ('gender', models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'no specify')], default=2)),
                ('photography', models.ImageField(blank=True, upload_to='', verbose_name='Photography')),
                ('client_type', models.IntegerField(choices=[(0, 'Patient'), (1, 'Doctor')], default=0)),
                ('description', models.TextField(blank=True, max_length=300, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
                'ordering': ['email'],
            },
            managers=[
                ('objects', users.models.managers.UserManager()),
            ],
        ),
    ]
