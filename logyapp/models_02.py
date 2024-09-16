
from django.db import models
from django.contrib.auth.models import User

class Appartement(models.Model):
    TYPES = (
        ('T1', 'T1'),
        ('T2', 'T2'),
        ('T3', 'T3'),
        ('T4', 'T4'),
        ('T5', 'T5'),
    )
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    type_appart = models.CharField(max_length=2, choices=TYPES)
    nb_couchages = models.IntegerField()
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appartements')
    description = models.TextField(blank=True)
    prix_nuit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nom} - {self.type_appart}"

class Reservation(models.Model):
    STATUTS = (
        ('CONFIRMEE', 'Confirmée'),
        ('EN_ATTENTE', 'En attente'),
        ('ANNULEE', 'Annulée'),
    )
    PLATEFORMES = (
        ('AIRBNB', 'Airbnb'),
        ('BOOKING', 'Booking'),
        ('AUTRE', 'Autre'),
    )
    appartement = models.ForeignKey(Appartement, on_delete=models.CASCADE, related_name='reservations')
    date_arrivee = models.DateField()
    date_depart = models.DateField()
    nom_client = models.CharField(max_length=100)
    email_client = models.EmailField()
    telephone_client = models.CharField(max_length=20)
    nb_personnes = models.IntegerField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')
    plateforme = models.CharField(max_length=20, choices=PLATEFORMES)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    commentaires = models.TextField(blank=True)

    def __str__(self):
        return f"Réservation {self.id} - {self.appartement.nom}"

class Tache(models.Model):
    TYPES = (
        ('MENAGE', 'Ménage'),
        ('MAINTENANCE', 'Maintenance'),
        ('ACCUEIL', 'Accueil'),
        ('AUTRE', 'Autre'),
    )
    STATUTS = (
        ('A_FAIRE', 'À faire'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
    )
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='taches')
    type_tache = models.CharField(max_length=20, choices=TYPES)
    description = models.TextField()
    date_prevue = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='A_FAIRE')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='taches_assignees')

    def __str__(self):
        return f"{self.type_tache} pour {self.reservation}"

class Facture(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='facture')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_emission = models.DateField(auto_now_add=True)
    date_paiement = models.DateField(null=True, blank=True)
    payee = models.BooleanField(default=False)

    def __str__(self):
        return f"Facture {self.id} pour la réservation {self.reservation.id}"