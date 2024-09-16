from django.contrib import admin

from django.contrib import admin
from .models import Locataire, Logement, Contrat, Paiement

@admin.register(Locataire)
class LocataireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone')
    search_fields = ('nom', 'prenom', 'email')

@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
    list_display = ('adresse', 'type_logement', 'superficie', 'loyer')
    list_filter = ('type_logement',)
    search_fields = ('adresse',)

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = ('locataire', 'logement', 'date_debut', 'date_fin', 'loyer_mensuel')
    list_filter = ('date_debut', 'date_fin')
    search_fields = ('locataire__nom', 'logement__adresse')

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('contrat', 'date_paiement', 'montant', 'methode_paiement')
    list_filter = ('date_paiement', 'methode_paiement')
    search_fields = ('contrat__locataire__nom', 'contrat__logement__adresse')
