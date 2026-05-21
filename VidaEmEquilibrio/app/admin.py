from django.contrib import admin
from .models import User, Psicologo, Paciente

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'tipo', 'ativo']
    search_fields = ['nome', 'email']

@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    list_display = ['get_nome', 'get_email', 'crp']
    search_fields = ['user__nome', 'user__email', 'crp']
    
    def get_nome(self, obj):
        return obj.user.nome
    get_nome.short_description = 'Nome'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['get_nome', 'get_email', 'get_psicologo']
    search_fields = ['user__nome', 'user__email']
    
    def get_nome(self, obj):
        return obj.user.nome
    get_nome.short_description = 'Nome'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_psicologo(self, obj):
        return obj.psicologo_responsavel.user.nome if obj.psicologo_responsavel else '-'
    get_psicologo.short_description = 'Psicólogo Responsável'
