from celery import shared_task 

from django.core.mail import send_mail

from citas.models import Cita

from C2D import settings 

@shared_task
def citaReminder(id):

    cita = Cita.objects.get(id=id)
    to = cita.patient.user.email

    subject = 'Recordatorio para su cita del dia de hoy'
    message = 'Su cita con el doctor es en 30 minutos'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to, ],
        fail_silently=False,
    )