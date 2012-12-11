# -*- coding: utf-8 -*-

from django.db import models

""" Gestion du contenu à savoir: l'actualité, les catégories
"""
class Categorie (models.Model):
    nom = models.CharField(max_length=64, verbose_name='Catégorie')
    date_categorie = models.DateField(verbose_name='Date de saisie')
    image_fond = models.CharField(max_length=64, blank=True, verbose_name='Image de dessus')
    ative = models.BooleanField()
    slug = models.SlugField(help_text='Texte pour diférencier les catégories')
    
    class Meta:
        ordering = ['nom']
        verbose_name = u"Catégorie"
        verbose_name_plural = u"Catégories"

    def __unicode__(self):
        return " %s %s %s" % (self.nom, self.image_fond, self.date_categorie)
       

class Actualite (models.Model):
    categorie = models.ForeignKey(Categorie)
    titre = models.CharField(max_length=128)
    resume = models.CharField(max_length=512, blank=True, verbose_name='resumé', default="")
    contenue = models.TextField(blank=True)
    image = models.ImageField(upload_to='actualites/images', blank=True, default="pas d'images")
    alt_img_text = models.CharField(max_length=256, verbose_name="texte alternative ", blank=True)
    date_saisie = models.DateField()
    defilante = models.BooleanField(blank=True)
    active = models.BooleanField()

    class Meta:
        ordering = ['date_saisie']
        verbose_name = u"Actualité"
        verbose_name_plural = u"Actualités"

    def __unicode__(self):
        return self.titre
 
    @models.permalink
    def get_absolute_url(self):
        return ('detail_actualites', [self.id,])





