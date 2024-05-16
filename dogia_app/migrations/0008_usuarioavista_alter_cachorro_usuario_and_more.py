# Generated by Django 4.2.11 on 2024-05-06 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogia_app', '0007_remove_usuario_data_criacao_remove_usuario_nome'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioAvista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('telefone', models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='cachorro',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cachorro',
            name='usuario_avista',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_avista', to='dogia_app.usuarioavista'),
        ),
    ]