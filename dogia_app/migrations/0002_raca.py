# Generated by Django 4.2.11 on 2024-04-06 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogia_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Raca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('data_criacao', models.DateTimeField()),
            ],
        ),
    ]
