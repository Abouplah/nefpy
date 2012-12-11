# -*- coding: utf-8 -*-
from django.db import models

from auf.django.references import models as ref

STATUT_CHOICES = ( 
        ('enseignant', 'Enseignant-chercheur dans un établissement'),
        ('etudiant', 'Étudiant-chercheur doctorant'),
        ('independant', 'Chercheur indépendant docteur'),
        ('expert', 'Expert')        
)

GENRE_CHOICES = (('m', 'Homme'), ('f', 'Femme')) 
DOMAINE_CHOICES = (
        ('9','Agronomie'), ('10', 'Biodiversité'), ('11', 'Changements climatiques'), ('3', 'Cultures'), 
        ('5','Cultures juridiques et gouvernance'), ('2', 'Didactiques'), ('14', 'Économie du développement'),
        ('12', 'Énergie'), ('7', 'Francophonie institutionnelle, État(s) francophone(s) et francophonie'),
        ('4', 'Langues pour le développement'), ('1', 'Littératures au Sud'), ('6', "Nouvelles figures de l'État"),
        ('8', 'Res@TICE'), ('15','Santé et bien-être des populations'), ('13', 'Ville durable'),
)
class ChercheurSearch(models.Model):
    q = models.CharField(max_length=255, blank=True, verbose_name="dans tous les champs")
    nom_chercheur = models.CharField(max_length=100, blank=True, verbose_name='nom')
    domaine = models.CharField(max_length=100, blank=True, choices=DOMAINE_CHOICES, verbose_name='domaine de recherche')
    statut = models.CharField(max_length=100, blank=True, choices=STATUT_CHOICES)
    discipline = models.ForeignKey(ref.Discipline, blank=True, null=True)
    pays = models.ForeignKey(ref.Pays, blank=True, null=True)
    etablissement = models.ForeignKey(ref.Etablissement, blank=True, null=True)
    activites_francophonie = models.CharField(max_length=25, blank=True, verbose_name='activités en Francophonie',
            choices=(('instance_auf', "Membre d'une instance de l'AUF"),
                ('expert_oif', "Sollicité par l'OIF"),
                ('association_francophone', "Membre d'une association ou d'une société savante francophone"),
                ('reseau_institutionnel', "Membre des instances d'un réseau institutionnel de l'AUF"))
    )
    genre = models.CharField(max_length=1, blank=True, choices=GENRE_CHOICES)