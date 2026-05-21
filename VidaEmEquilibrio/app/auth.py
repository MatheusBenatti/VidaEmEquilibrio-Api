from django.contrib.auth.hashers import check_password
from .models import User

def authenticate_user(email, senha):
    """
    Autentica qualquer tipo de usuário (psicólogo ou paciente)
    Email é usado como username
    Retorna: (token, user) ou (None, None)
    """
    try:
        user = User.objects.get(username=email)
        
        # Verifica a senha
        if check_password(senha, user.password) and user.ativo:
            # Gera token se não existir
            if not user.token:
                import secrets
                user.token = secrets.token_hex(20)
                user.save()
            
            return user.token, user
        else:
            return None, None
    except User.DoesNotExist:
        return None, None