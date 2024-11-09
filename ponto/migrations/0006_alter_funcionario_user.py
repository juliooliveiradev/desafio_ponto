# Generated by Django 5.1.3 on 2024-11-08 18:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0005_funcionario_user_alter_ponto_entrada_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to=settings.AUTH_USER_MODEL),
        ),
    ]
