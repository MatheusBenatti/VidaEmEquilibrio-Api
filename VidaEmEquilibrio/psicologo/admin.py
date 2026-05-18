from django.contrib import admin
from .models import Psicologo

@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'crp', 'ativo']
    search_fields = ['nome', 'email', 'crp']
