from django.db import models
from doctors.models import Doctor
from patients.models import Patient 

# Create your models here.

class Cita(models.Model):
    
    date_time = models.DateTimeField(blank=True, null=True)
    accept = models.BooleanField(blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    appointment_type = models.CharField(max_length=50, blank=True, null=True)
    appointment_reason = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    room = models.CharField(max_length=12, blank=True, null = True)
    
    def __str__(self):
        return 'Cita para el dia %s' % self.date_time
        
    class Meta:
        db_table = 'citas'
