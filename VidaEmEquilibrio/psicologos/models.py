from django.db import models
from django.contrib.auth.hashers import make_password

class Psicologo(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    crp = models.CharField(max_length=20, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk:  # Only hash on creation
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Psicologo'
        verbose_name_plural = 'Psicologos'
        db_table = 'psicologo'
