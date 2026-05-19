from rest_framework.authtoken.models import Token
from .models import Psicologo
from django.contrib.auth.hashers import check_password

def authenticate_psicologo(email, senha):
    """
    Autentica um psicólogo e retorna o token
    """
    try:
        psicologo = Psicologo.objects.get(email=email)
        
        # Verifica a senha
        if check_password(senha, psicologo.senha):
            # Gera ou pega o token
            token, created = Token.objects.get_or_create(user_id=psicologo.id)
            return token.key, psicologo
        else:
            return None, None
    except Psicologo.DoesNotExist:
        return None, None
