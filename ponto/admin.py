# ponto/admin.py
from django.contrib import admin
from .models import Empresa, Funcionario, Ponto

# Registre seus modelos no admin
admin.site.register(Empresa)
admin.site.register(Funcionario)
admin.site.register(Ponto)

