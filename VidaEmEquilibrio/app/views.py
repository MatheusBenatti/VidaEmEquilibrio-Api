from rest_framework import viewsets, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import check_password
from .models import User, Psicologo, Paciente
from .auth import authenticate_user
from .serializers import (
    PsicologoSerializer, PacienteSerializer,
    RegistroPsicologoSerializer, RegistroPacienteSerializer, LoginSerializer
)
import secrets


def get_user_from_token(request):
    """Extrai o usuário a partir do header Authorization: Token <token>"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Token '):
        return None
    token = auth_header.split('Token ')[1].strip()
    try:
        return User.objects.get(token=token)
    except User.DoesNotExist:
        return None


class PsicologoViewSet(viewsets.ModelViewSet):
    queryset = Psicologo.objects.all()
    serializer_class = PsicologoSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):

    email = request.data.get('email')
    senha = request.data.get('senha')
    
    if not email or not senha:
        return Response(
            {'error': 'Email e senha são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token, user = authenticate_user(email, senha)
    
    if token:
        data = {
            'token': token,
            'id': user.id,
            'nome': user.nome,
            'username': user.username,
            'tipo': user.tipo,
            'primeira_senha': user.primeira_senha,
        }
        
        if user.tipo == 'psicologo' and hasattr(user, 'psicologo_profile'):
            data['crp'] = user.psicologo_profile.crp
        
        return Response(data)
    else:
        return Response(
            {'error': 'Email ou senha inválidos'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def registrar_psicologo(request):

    serializer = RegistroPsicologoSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                'success': 'Psicólogo cadastrado com sucesso',
                'id': user.id,
                'email': user.username,
                'tipo': user.tipo,
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def registrar_paciente(request):

    serializer = RegistroPacienteSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                'success': 'Paciente cadastrado com sucesso',
                'id': user.id,
                'email': user.username,
                'tipo': user.tipo,
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def adicionar_paciente(request):
    user = get_user_from_token(request)
    if not user:
        return Response({'error': 'Não autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        psicologo_profile = Psicologo.objects.get(user=user)
    except Psicologo.DoesNotExist:
        return Response({'error': 'Psicólogo não encontrado'}, status=status.HTTP_403_FORBIDDEN)
    
    email = request.data.get('email')
    nome = request.data.get('nome', 'Paciente')
    
    if not email:
        return Response({'error': 'Email obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=email).exists():
        return Response({'error': 'Email já cadastrado'}, status=status.HTTP_400_BAD_REQUEST)
    
    senha_temporaria = secrets.token_urlsafe(8)
    
    paciente_user = User.objects.create_user(
        username=email,
        password=senha_temporaria,
        nome=nome,
        tipo='paciente',
        primeira_senha=True,
    )
    
    paciente = Paciente.objects.create(
        user=paciente_user,
        psicologo_responsavel=psicologo_profile
    )
    
    # Enviar email
    try:
        enviar_email_convite(email, nome, senha_temporaria)
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
    
    return Response({
        'success': 'Paciente adicionado',
        'id': paciente_user.id,
        'username': paciente_user.username,
        'nome': paciente_user.nome,
        'senha_temporaria': senha_temporaria,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def meus_pacientes(request):
    user = get_user_from_token(request)
    if not user:
        return Response({'error': 'Não autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        psicologo_profile = Psicologo.objects.get(user=user)
    except Psicologo.DoesNotExist:
        return Response({'error': 'Psicólogo não encontrado'}, status=status.HTTP_403_FORBIDDEN)
    
    pacientes = Paciente.objects.filter(psicologo_responsavel=psicologo_profile).select_related('user')
    data = []
    for p in pacientes:
        data.append({
            'id': p.id,
            'nome': p.user.nome,
            'email': p.user.username,
        })
    
    return Response(data)


def enviar_email_convite(email, nome, senha_temporaria):

    assunto = 'Convite para Vida em Equilíbrio'
    mensagem = f"""
    Olá {nome}!
    
    Você foi convidado para fazer parte da plataforma Vida em Equilíbrio.
    
    Seus dados de acesso:
    Email: {email}
    Senha Temporária: {senha_temporaria}
    
    Acesse em: http://localhost:3000/login
    
    Na primeira vez, você será solicitado a criar uma nova senha.
    
    Atenciosamente,
    Vida em Equilíbrio
    """
    
    send_mail(
        assunto,
        mensagem,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def mudar_senha(request):

    user = get_user_from_token(request)
    if not user:
        return Response({'error': 'Não autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
    
    senha_atual = request.data.get('senha_atual')
    nova_senha = request.data.get('nova_senha')
    
    if not senha_atual or not nova_senha:
        return Response(
            {'error': 'Senha atual e nova são obrigatórias'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not check_password(senha_atual, user.password):
        return Response(
            {'error': 'Senha atual incorreta'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user.set_password(nova_senha)
    user.primeira_senha = False
    user.save()
    
    return Response({'success': 'Senha alterada com sucesso'})