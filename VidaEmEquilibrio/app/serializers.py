from rest_framework import serializers
from .models import User, Psicologo, Paciente

class UserSerializer(serializers.ModelSerializer):
    """Serializer para dados públicos do usuário"""
    class Meta:
        model = User
        fields = ['id', 'email', 'nome', 'tipo']


class PsicologoSerializer(serializers.ModelSerializer):
    """Serializer para perfil de psicólogo"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Psicologo
        fields = ['id', 'user', 'crp']


class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para perfil de paciente"""
    user = UserSerializer(read_only=True)
    psicologo_responsavel = PsicologoSerializer(read_only=True)
    
    class Meta:
        model = Paciente
        fields = ['id', 'user', 'psicologo_responsavel']


class RegistroPsicologoSerializer(serializers.ModelSerializer):
    """Serializer para registro de psicólogo"""
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.EmailField()  # Username é email
    nome = serializers.CharField(max_length=150)
    crp = serializers.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'nome', 'crp']
    
    def create(self, validated_data):
        crp = validated_data.pop('crp')
        nome = validated_data.pop('nome')
        username = validated_data.pop('username')
        
        user = User.objects.create_user(
            username=username,
            password=validated_data['password'],
            nome=nome,
            tipo='psicologo',
        )
        
        # Cria perfil de psicólogo
        Psicologo.objects.create(user=user, crp=crp)
        
        return user


class RegistroPacienteSerializer(serializers.ModelSerializer):
    """Serializer para registro de paciente"""
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.EmailField()  # Username é email
    nome = serializers.CharField(max_length=150)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'nome']
    
    def create(self, validated_data):
        nome = validated_data.pop('nome')
        username = validated_data.pop('username')
        
        user = User.objects.create_user(
            username=username,
            password=validated_data['password'],
            nome=nome,
            tipo='paciente',
        )
        
        # Cria perfil de paciente
        Paciente.objects.create(user=user)
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)