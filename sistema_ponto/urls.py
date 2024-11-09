# sistema_ponto/urls.py
from django.contrib import admin  # Importando o admin do Django
from django.urls import path
from django.contrib.auth import views as auth_views
from ponto import views  # Importando as views da app ponto

urlpatterns = [
    path('admin/', admin.site.urls),  # Usando o admin do Django
    path('', views.home, name='home'),
    path('cadastrar_empresa/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('cadastrar_funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('registrar_ponto/', views.registrar_ponto, name='registrar_ponto'),
    path('consultar_ponto/', views.consultar_ponto, name='consultar_ponto'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
