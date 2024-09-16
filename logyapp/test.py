from django.test import TestCase
from django.contrib.auth.models import User
from .models import Property, Listing, Reservation

class PropertyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = Property.objects.create(
            name='Test Property',
            type='Apartment',
            address='123 Test St',
            owner=self.user
        )

    def test_property_creation(self):
        self.assertEqual(self.property.name, 'Test Property')
        self.assertEqual(self.property.owner, self.user)

class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = Property.objects.create(
            name='Test Property',
            type='Apartment',
            address='123 Test St',
            owner=self.user
        )
        self.listing = Listing.objects.create(
            property=self.property,
            platform='airbnb',
            listing_url='https://airbnb.com/test',
            is_active=True
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.property, self.property)
        self.assertEqual(self.listing.platform, 'airbnb')

class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = Property.objects.create(
            name='Test Property',
            type='Apartment',
            address='123 Test St',
            owner=self.user
        )
        self.reservation = Reservation.objects.create(
            property=self.property,
            start_date='2024-01-01',
            end_date='2024-01-07',
            guest_name='John Doe',
            guest_email='john@example.com'
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.property, self.property)
        self.assertEqual(self.reservation.guest_name, 'John Doe')