from rest_framework import serializers
from .models import Psicologo

class PsicologoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psicologo
        fields = ['id', 'nome', 'email', 'crp']