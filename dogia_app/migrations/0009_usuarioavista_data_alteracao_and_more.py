# Generated by Django 4.2.11 on 2024-05-06 15:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dogia_app', '0008_usuarioavista_alter_cachorro_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioavista',
            name='data_alteracao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuarioavista',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]