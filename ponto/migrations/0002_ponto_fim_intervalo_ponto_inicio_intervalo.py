# Generated by Django 5.1.3 on 2024-11-08 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ponto',
            name='fim_intervalo',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ponto',
            name='inicio_intervalo',
            field=models.TimeField(blank=True, null=True),
        ),
    ]