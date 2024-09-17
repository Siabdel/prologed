
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from logyapp import models as cg_models

class PropertyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test Villa",
            type="villa",
            address="123 Test St, Test City",
            owner=self.user,
            price_per_night=Decimal('100.00')
        )

    def test_property_creation(self):
        self.assertEqual(self.property.name, "Test Villa")
        self.assertEqual(self.property.owner, self.user)

    def test_get_active_listings(self):
        cg_models.Listing.objects.create(
            property=self.property,
            platform='airbnb',
            listing_url='http://test.com',
            is_active=True
        )
        cg_models.Listing.objects.create(
            property=self.property,
            platform='booking',
            listing_url='http://test2.com',
            is_active=False
        )
        active_listings = self.property.get_active_listings()
        self.assertEqual(active_listings.count(), 1)

class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test House",
            type="house",
            address="456 Test Ave, Test Town",
            owner=self.user,
            price_per_night=Decimal('150.00')
        )
        self.listing = cg_models.Listing.objects.create(
            property=self.property,
            platform='airbnb',
            listing_url='http://test.com',
            is_active=True
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.property, self.property)
        self.assertEqual(self.listing.platform, 'airbnb')
        self.assertTrue(self.listing.is_active)

    def test_deactivate_listing(self):
        self.listing.deactivate()
        self.assertFalse(self.listing.is_active)

class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test House",
            type="house",
            address="456 Test Ave, Test Town",
            owner=self.user,
            price_per_night=Decimal('150.00')
        )
        self.reservation = cg_models.Reservation.objects.create(
            property=self.property,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=3),
            guest_name="John Doe",
            guest_email="john@example.com",
            number_of_guests=2,
            cleaning_fee=Decimal('50.00'),
            service_fee=Decimal('30.00')
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.guest_name, "John Doe")
        self.assertEqual(self.reservation.number_of_guests, 2)

    def test_get_duration(self):
        self.assertEqual(self.reservation.get_duration(), 3)

    def test_calculate_total_price(self):
        expected_total = (Decimal('150.00') * 3) + Decimal('50.00') + Decimal('30.00')
        self.assertEqual(self.reservation.calculate_total_price(), expected_total)

class MaintenanceTaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test Apartment",
            type="apartment",
            address="789 Test Blvd, Test City",
            owner=self.user
        )
        self.task = cg_models.MaintenanceTask.objects.create(
            property=self.property,
            maintenance_type='cleaning',
            description="Deep clean after checkout",
            due_date=timezone.now().date() + timezone.timedelta(days=1)
        )

    def test_maintenance_task_creation(self):
        self.assertEqual(self.task.maintenance_type, 'cleaning')
        self.assertFalse(self.task.completed)

    def test_mark_as_completed(self):
        self.task.mark_as_completed()
        self.assertTrue(self.task.completed)

class EmergencyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test Villa",
            type="villa",
            address="123 Emergency St, Test City",
            owner=self.user
        )
        self.emergency = cg_models.Emergency.objects.create(
            property=self.property,
            description="Water leak in bathroom"
        )

    def test_emergency_creation(self):
        self.assertIsNotNone(self.emergency.reported_at)
        self.assertIsNone(self.emergency.resolved_at)

    def test_resolve_emergency(self):
        self.emergency.resolve()
        self.assertIsNotNone(self.emergency.resolved_at)

class PricingRuleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test House",
            type="house",
            address="456 Pricing Ave, Test Town",
            owner=self.user
        )
        self.pricing_rule = cg_models.PricingRule.objects.create(
            property=self.property,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=30),
            price_per_night=Decimal('200.00')
        )

    def test_pricing_rule_creation(self):
        self.assertEqual(self.pricing_rule.price_per_night, Decimal('200.00'))

    def test_is_active(self):
        self.assertTrue(self.pricing_rule.is_active())

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employee', password='12345')
        self.employee = cg_models.Employee.objects.create(
            user=self.user,
            role='cleaner',
            phone_number='1234567890',
            hire_date=timezone.now().date()
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.role, 'cleaner')
        self.assertTrue(self.employee.is_active)

class AvailabilityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test Condo",
            type="apartment",
            address="789 Available St, Test City",
            owner=self.user
        )
        self.availability = cg_models.Availability.objects.create(
            property=self.property,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=7),
            is_available=True
        )

    def test_availability_creation(self):
        self.assertTrue(self.availability.is_available)
        self.assertEqual(self.availability.property, self.property)

class ScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employee', password='12345')
        self.employee = cg_models.Employee.objects.create(
            user=self.user,
            role='cleaner',
            phone_number='1234567890',
            hire_date=timezone.now().date()
        )
        self.schedule = cg_models.Schedule.objects.create(
            employee=self.employee,
            date=timezone.now().date(),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=8)).time()
        )

    def test_schedule_creation(self):
        self.assertEqual(self.schedule.employee, self.employee)
        self.assertIsNotNone(self.schedule.start_time)
        self.assertIsNotNone(self.schedule.end_time)

class ServiceTaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test House",
            type="house",
            address="123 Service St, Test City",
            owner=self.user
        )
        self.service_task = cg_models.ServiceTask.objects.create(
            property=self.property,
            service_type='check_in',
            description="Welcome guest and provide keys",
            due_date=timezone.now() + timezone.timedelta(days=1)
        )

    def test_service_task_creation(self):
        self.assertEqual(self.service_task.service_type, 'check_in')
        self.assertFalse(self.service_task.completed)

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test Property",
            type="apartment",
            address="123 Payment St, Test City",
            owner=self.user,
            price_per_night=Decimal('100.00')
        )
        self.reservation = cg_models.Reservation.objects.create(
            property=self.property,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=2),
            guest_name="Jane Doe",
            guest_email="jane@example.com",
            total_price=Decimal('250.00')
        )
        self.payment = cg_models.Payment.objects.create(
            reservation=self.reservation,
            amount=Decimal('250.00')
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, Decimal('250.00'))
        self.assertFalse(self.payment.is_refund)

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.property = cg_models.Property.objects.create(
            name="Test Property",
            type="apartment",
            address="123 Review St, Test City",
            owner=self.user,
            price_per_night=Decimal('100.00')
        )
        self.reservation = cg_models.Reservation.objects.create(
            property=self.property,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=2),
            guest_name="Alice Smith",
            guest_email="alice@example.com",
            total_price=Decimal('250.00')
        )
        self.review = cg_models.Review.objects.create(
            reservation=self.reservation,
            rating=5,
            comment="Excellent stay!"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Excellent stay!")
        self.assertEqual(self.review.reservation, self.reservation)