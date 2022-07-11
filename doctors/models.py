from django.db import models
from users.models import User
from datetime import datetime

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  
    curp = models.CharField(max_length=18, verbose_name = "CFCI")
    fiscal_address = models.CharField(max_length=50, verbose_name = "Fiscal address")
    rfc = models.CharField(max_length=15, verbose_name = "RFC")
    cfdi = models.CharField(max_length=50, verbose_name = "CFDI")

    university = models.CharField(max_length=150, verbose_name = "Universidad")
    professional_license = models.CharField(max_length=15, verbose_name = "Professional license")

    speciality = models.CharField(max_length=100, verbose_name = "Speciality")

    postgraduate = models.CharField(max_length=100, verbose_name = "Postgraduate")

    address = models.CharField(max_length=150, verbose_name = "Address")
    contact_phone = models.CharField(max_length=13, verbose_name = "Contact phone")
    reference = models.CharField(max_length=50, verbose_name = "Reference")

    name_account_owner = models.CharField(max_length=75, verbose_name = "Name account owner")
    bank = models.CharField(max_length=75, verbose_name = "Bank")
    account = models.CharField(max_length = 20, verbose_name = "Account")
    clabe = models.CharField(max_length = 18, verbose_name = "CLABE")
    
    def __str__(self):
        return self.user.name
    
    class Meta:
        db_table = 'doctors'
        ordering = ['speciality',]
        
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    month = models.CharField(max_length=50)
    day = models.CharField(max_length=50)
    year = models.IntegerField(default=datetime.now().year)
    hour1 = models.TimeField(null=True,auto_now=False, auto_now_add=False)
    hour2 = models.TimeField(null=True,auto_now=False, auto_now_add=False)
    hour3 = models.TimeField(null=True,auto_now=False, auto_now_add=False)
    hour4 = models.TimeField(null=True,auto_now=False, auto_now_add=False)
    hour5 = models.TimeField(null=True,auto_now=False, auto_now_add=False)
    hour6 = models.TimeField(null=True,auto_now=False, auto_now_add=False)
    hour7 = models.TimeField(null=True,auto_now=False, auto_now_add=False)
    hour9 = models.TimeField(null=True,auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.doctor
    
    class Meta:
        db_table = 'Schedule'
        ordering = ['month',]


