from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PsicologoViewSet, login_psicologo

router = DefaultRouter()
router.register(r'psicologos', PsicologoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_psicologo, name='login_psicologo'),
]