from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from .models import Locataire, Logement, Contrat, Paiement

class LocataireModelTest(TestCase):
    def test_create_locataire(self):
        locataire = Locataire.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            telephone="0123456789"
        )
        self.assertEqual(str(locataire), "Jean Dupont")

class LogementModelTest(TestCase):
    def test_create_logement(self):
        logement = Logement.objects.create(
            adresse="123 Rue de la Paix",
            type_logement="Appartement",
            superficie=50,
            loyer=800
        )
        self.assertEqual(str(logement), "123 Rue de la Paix")

class ContratModelTest(TestCase):
    def setUp(self):
        self.locataire = Locataire.objects.create(nom="Dupont", prenom="Jean")
        self.logement = Logement.objects.create(adresse="123 Rue de la Paix", loyer=800)

    def test_create_contrat(self):
        contrat = Contrat.objects.create(
            locataire=self.locataire,
            logement=self.logement,
            date_debut="2024-01-01",
            date_fin="2024-12-31",
            loyer_mensuel=800
        )
        self.assertEqual(str(contrat), "Contrat de Jean Dupont pour 123 Rue de la Paix")

class PaiementModelTest(TestCase):
    def setUp(self):
        locataire = Locataire.objects.create(nom="Dupont", prenom="Jean")
        logement = Logement.objects.create(adresse="123 Rue de la Paix", loyer=800)
        self.contrat = Contrat.objects.create(
            locataire=locataire,
            logement=logement,
            date_debut="2024-01-01",
            date_fin="2024-12-31",
            loyer_mensuel=800
        )

    def test_create_paiement(self):
        paiement = Paiement.objects.create(
            contrat=self.contrat,
            date_paiement="2024-02-01",
            montant=800,
            methode_paiement="Virement"
        )
        self.assertEqual(str(paiement), "Paiement de 800 € pour le contrat de Jean Dupont")

