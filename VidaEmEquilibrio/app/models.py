from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets

class User(AbstractUser):
    TIPO_CHOICES = [
        ('psicologo', 'Psicólogo'),
        ('paciente', 'Paciente'),
    ]

    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    token = models.CharField(max_length=40, unique=True, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    primeira_senha = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'usuarios'
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    
    def save(self, *args, **kwargs):
        # Gera token se for novo e não tiver
        if not self.pk and not self.token:
            self.token = secrets.token_hex(20)
        super().save(*args, **kwargs)


class Psicologo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='psicologo_profile')
    crp = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'psicologo_profile'
    
    def __str__(self):
        return f"Dra/Dr. {self.user.nome}"


class Paciente(models.Model):
    AVATAR_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente_profile')
    psicologo_responsavel = models.ForeignKey(
        Psicologo, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='pacientes'
    )
    avatar = models.CharField(max_length=20, choices=AVATAR_CHOICES, null=True, blank=True)
    perfil_configurado = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'paciente_profile'
    
    def __str__(self):
        return self.user.nome