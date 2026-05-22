from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PsicologoViewSet, PacienteViewSet,
    login, registrar_psicologo, registrar_paciente,
    adicionar_paciente, mudar_senha, meus_pacientes, configurar_perfil,
    salvar_relato, relatos_paciente
)

router = DefaultRouter()
router.register(r'psicologos', PsicologoViewSet)
router.register(r'pacientes', PacienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login, name='login'),
    path('registrar-psicologo/', registrar_psicologo, name='registrar_psicologo'),
    path('registrar-paciente/', registrar_paciente, name='registrar_paciente'),
    path('adicionar-paciente/', adicionar_paciente, name='adicionar_paciente'),
    path('mudar-senha/', mudar_senha, name='mudar_senha'),
    path('meus-pacientes/', meus_pacientes, name='meus_pacientes'),
    path('configurar-perfil/', configurar_perfil, name='configurar_perfil'),
    path('salvar-relato/', salvar_relato, name='salvar_relato'),
    path('relatos-paciente/<int:paciente_id>/', relatos_paciente, name='relatos_paciente'),
]