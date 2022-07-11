from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.
GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'no specify'),
)

CLIENT_CHOICES = (
    (0, 'Patient'),
    (1, 'Doctor'),
)

class User(AbstractUser):
    username = None

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique' : 'Email already exists.'
        }
    )

    name = models.CharField(max_length=50, blank = False, null = False, verbose_name="Name")
    first_name = models.CharField(max_length=50,blank = False, null = False, verbose_name="First name")
    last_name = models.CharField(max_length=50, blank = False, null = False, verbose_name="Last name")
    birthday = models.CharField(max_length = 12, blank = False, null = False, verbose_name="Birthday")
    phone = models.CharField(max_length=10, blank = False , null = False, verbose_name="Phone")
    gender = models.IntegerField(choices=GENDER_CHOICES, default = 2)
    photography=models.ImageField(blank=True,null=False, verbose_name="Photography")
    client_type = models.IntegerField(choices=CLIENT_CHOICES, default = 0)
    description=models.TextField(max_length=300, blank=True,null=False, verbose_name="Description")
    is_active = models.BooleanField(default = True, verbose_name="Is active")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
         return 'Email %s of Name: %s'%(self.email, self.name);

    class Meta:
        db_table = 'users'
        ordering = ['email',]
