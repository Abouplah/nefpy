# -=- encoding: utf-8 -=-

from django.contrib import admin

from models import Categorie, Actualite

class ActualiteAdmin(admin.ModelAdmin):
    search_fields = ('titre',)
    list_display = ('titre', 'categorie',)
    list_filter = ('categorie',)
    date_hierarchy = 'date_saisie'        

class CategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nom",)}
    search_fields = ('nom',)
    list_display = ('nom','date_categorie',)
    list_filter = ('date_categorie',)
    date_hierarchy = 'date_categorie'
    

admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Actualite, ActualiteAdmin)