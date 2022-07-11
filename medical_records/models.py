from django.db import models 

from patients.models import Patient

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, null=True)

    important_background = models.TextField(max_length=400)
    allergies = models.CharField(max_length=254)
    reference = models.CharField(max_length=100, blank=True, null=True)

    patient_observations = models.CharField(max_length=254, blank=True, null=True)

    family_background = models.TextField(max_length=400)

    pathological_background = models.CharField(max_length=250)
    currently_medication = models.CharField(max_length=250, blank=True, null=True)
    surgeries = models.CharField(max_length=250, blank=True, null=True)

    nonpath_background = models.CharField(max_length=250)
    smoking = models.BooleanField(blank=True, null=True)
    drinking = models.BooleanField(blank=True, null=True)

    gynecological_background = models.CharField(max_length=250, blank=True, null=True)
    system_interrogation = models.CharField(max_length=250, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Historial medico del paciente %s' % self.patient

    class Meta:
        db_table = 'Medical Records'