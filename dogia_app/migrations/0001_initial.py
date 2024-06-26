# Generated by Django 4.2.11 on 2024-04-16 23:36

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import dogia_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cachorro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default=None, max_length=50)),
                ('genero', models.SmallIntegerField(choices=[(1, 'Macho'), (2, 'Fêmea')])),
                ('status', models.BooleanField(default=True)),
                ('tipo', models.SmallIntegerField(choices=[(1, 'Buscado'), (2, 'Avistado')], default=1)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_alteracao', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Raca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_alteracao', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('telefone', models.CharField(default='', max_length=15)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_alteracao', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Imagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caminho', models.ImageField(upload_to=dogia_app.models.generate_filename)),
                ('embedding', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_alteracao', models.DateTimeField(blank=True, null=True)),
                ('cachorro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cachorro', to='dogia_app.cachorro')),
            ],
        ),
        migrations.CreateModel(
            name='Combinacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('score_bruto', models.FloatField()),
                ('distancia', models.FloatField()),
                ('distancia_bruta', models.FloatField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_alteracao', models.DateTimeField(blank=True, null=True)),
                ('id_avistado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avistado', to='dogia_app.cachorro')),
                ('id_buscado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buscado', to='dogia_app.cachorro')),
            ],
        ),
        migrations.AddField(
            model_name='cachorro',
            name='raca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raca', to='dogia_app.raca'),
        ),
        migrations.AddField(
            model_name='cachorro',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='dogia_app.usuario'),
        ),
    ]
