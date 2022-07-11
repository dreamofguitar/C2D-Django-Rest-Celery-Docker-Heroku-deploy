from django.contrib import admin

from citas_express.models import CitaExpress

@admin.register(CitaExpress)
class CitaExpAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')