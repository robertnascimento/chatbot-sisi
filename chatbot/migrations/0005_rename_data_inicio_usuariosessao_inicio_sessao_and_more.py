# Generated by Django 5.0.7 on 2024-08-26 21:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_usuariosessao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuariosessao',
            old_name='data_inicio',
            new_name='inicio_sessao',
        ),
        migrations.AlterField(
            model_name='usuariosessao',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot.curso'),
        ),
    ]
