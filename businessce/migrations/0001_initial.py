# Generated by Django 2.2.13 on 2020-11-24 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoOf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_of', models.CharField(max_length=20, unique=True)),
                ('statut', models.CharField(max_length=1)),
                ('type_of', models.CharField(max_length=1)),
                ('commande', models.CharField(max_length=20, unique=True)),
                ('article', models.CharField(max_length=20, unique=True)),
                ('code_form_prod_id', models.CharField(blank=True, max_length=5, null=True)),
                ('code_form_cond_id', models.CharField(blank=True, max_length=5, null=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_by', models.CharField(max_length=100)),
                ('close_by', models.CharField(blank=True, max_length=100, null=True)),
                ('machine', models.CharField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('numero_priorite', models.IntegerField()),
                ('semaine', models.CharField(max_length=2)),
                ('annee', models.CharField(max_length=4)),
                ('date_debut_planifiee', models.DateTimeField(blank=True, null=True)),
                ('date_fin_planifiee', models.DateTimeField(blank=True, null=True)),
                ('date_debut_reelle', models.DateTimeField()),
                ('date_fin_reelle', models.DateTimeField(blank=True, null=True)),
                ('date_cloture', models.DateTimeField(blank=True, null=True)),
                ('quantite_commandee', models.FloatField()),
                ('quantite_realisee', models.FloatField(blank=True, null=True)),
                ('quantite_restante', models.FloatField()),
                ('quantite_prevue', models.FloatField()),
                ('unite_quantite', models.CharField(max_length=1)),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_livraison_prevue', models.DateTimeField(blank=True, null=True)),
                ('code_atelier_id', models.CharField(max_length=2)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.DjangoClient')),
            ],
            options={
                'db_table': 'ordre_fabrication',
                'ordering': ['-date_debut_reelle'],
                'managed': True,
            },
        ),
    ]
