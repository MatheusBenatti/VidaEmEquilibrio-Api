from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Psicologo
from .serializers import PsicologoSerializer
from .auth import authenticate_psicologo


class PsicologoViewSet(viewsets.ModelViewSet):
    queryset = Psicologo.objects.all()
    serializer_class = PsicologoSerializer


@api_view(['POST'])
def login_psicologo(request):
    """
    Login customizado para psicólogos usando email e senha
    """
    email = request.data.get('email')
    senha = request.data.get('senha')
    
    if not email or not senha:
        return Response(
            {'error': 'Email e senha são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token, psicologo = authenticate_psicologo(email, senha)
    
    if token:
        return Response({
            'token': token,
            'id': psicologo.id,
            'nome': psicologo.nome,
            'email': psicologo.email,
            'crp': psicologo.crp,
        })
    else:
        return Response(
            {'error': 'Email ou senha inválidos'},
            status=status.HTTP_401_UNAUTHORIZED
        )