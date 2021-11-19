# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from projects.models import DjangoClient

# Create your models here.

# Table Ordre Fabrication

class DjangoOf(models.Model):
    code_of = models.CharField(max_length=20, unique=True)
    statut = models.CharField(max_length=1)
    type_of = models.CharField(max_length=1)
    client = models.ForeignKey(DjangoClient, to_field='codeclie',  blank=True, null=True, on_delete=models.SET_NULL)
    commande = models.CharField(max_length=20, unique=True)
    article = models.CharField(max_length=20, unique=True)

    code_form_prod_id = models.CharField( max_length=5, blank=True,  null=True)  # code formule Fabrication
    code_form_cond_id = models.CharField(
        max_length=5,  blank=True, null=True)  # code formule condit
    created_by = models.CharField(max_length=100)
    modified_by = models.CharField(max_length=100)
    close_by = models.CharField(max_length=100,   blank=True, null=True)
    machine = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    numero_priorite = models.IntegerField()
    semaine = models.CharField(max_length=2)
    annee = models.CharField(max_length=4)
    date_debut_planifiee = models.DateTimeField(
        auto_now=False, blank=True, null=True)
    date_fin_planifiee = models.DateTimeField(
        auto_now=False, blank=True, null=True)
    date_debut_reelle = models.DateTimeField(auto_now=False)
    date_fin_reelle = models.DateTimeField(
        auto_now=False, blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    quantite_commandee = models.FloatField()
    quantite_realisee = models.FloatField(blank=True, null=True)
    quantite_restante = models.FloatField()
    quantite_prevue = models.FloatField()
    unite_quantite = models.CharField(max_length=1)
    comment = models.TextField(blank=True, null=True)
    date_livraison_prevue = models.DateTimeField(blank=True, null=True)
    code_atelier_id = models.CharField(max_length=2)
    #pd_objects = DataFrameManager()  # Pandas-Enabled Manager

    class Meta:
        managed  = True
        db_table  = 'ordre_fabrication'
        ordering = ['-date_debut_reelle']

    def __unicode__(self):
        return u'code of=%s' % self.code_of

    def save_of(self):
        # self.semaine = get_num_semaine_from_date(self.date_debut_reelle.strftime('%Y'), self.date_debut_reelle.strftime('%m'), self.date_debut_reelle.strftime('%d'))
        # self.annee   = self.date_debut_reelle.strftime('%Y')
        if self.statut in ('P', 'C', 'D'):
            self.annee = str(datetime.isocalendar(
                self.date_debut_reelle)[0])[-2:]
            self.semaine = str(datetime.isocalendar(self.date_debut_reelle)[1])
            # complete semaine a 2 cars
            self.semaine = self.semaine.zfill(2)
            # mise a jour du plan de charge PDC (tmpcharc)
            # self.pdc.ancond     = self.annee
            # self.pdc.dcondsce   = self.semaine
            # save pdc
            # if you want only to update model if exist (without create it):

            # self.pdc.save()
            # save of
            return self.save()

        return False
