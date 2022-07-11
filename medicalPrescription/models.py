from django.db import models
from doctors.models import Doctor
from patients.models import Patient 


class Prescription(models.Model):
    
    clinical_note = models.CharField(max_length=2000)
    prescription = models.CharField(max_length=2000)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return 'Prescripcion Medica de  %s' % self.patient

    class Meta:
        db_table = 'medicalPrescription'