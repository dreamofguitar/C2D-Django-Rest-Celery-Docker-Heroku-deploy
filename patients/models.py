from django.db import models
from users.models import User
# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    patient_description = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name
        
    class Meta:
        db_table = 'patients'
       