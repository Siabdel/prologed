from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    address = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Listing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)  # e.g., Airbnb, Booking
    listing_url = models.URLField()
    is_active = models.BooleanField(default=True)

class Reservation(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()

class MaintenanceTask(models.Model):
    TASK_TYPES = [
        ('cleaning', 'Cleaning'),
        ('laundry', 'Laundry'),
        ('repair', 'Repair'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

class Emergency(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

class PricingRule(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

class Report(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    month = models.DateField()
    occupancy_rate = models.FloatField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()  # JSON or formatted text for detailed report
