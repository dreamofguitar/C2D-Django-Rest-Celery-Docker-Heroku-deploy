from django.db import models

from patients.models import Patient 

from doctors.models import Doctor

class CitaExpress(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_reason = models.CharField(max_length=200)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)

    completed = models.BooleanField(default=False)

    taken = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Cita general del paciente %s' % self.patient