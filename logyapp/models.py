
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Property(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    address = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Ajoutez cette ligne

    def __str__(self):
        return f"{self.name} ({self.type})"

    def get_active_listings(self):
        return self.listing_set.filter(is_active=True)

    def get_upcoming_reservations(self):
        return self.reservations_set.filter(start_date__gte=timezone.now().date())

class Listing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='listings')
    platform = models.CharField(max_length=50)
    listing_url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.property.name} on {self.platform}"

    def deactivate(self):
        self.is_active = False
        self.save()

class Reservation(models.Model):
    RESERVATION_STATUS = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]
    
    PLATFORM_CHOICES = [
        ('airbnb', 'Airbnb'),
        ('booking', 'Booking.com'),
        ('direct', 'Direct Booking'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, 
                                            related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    
    # Nouveaux champs
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, null=True)
    reservation_status = models.CharField(max_length=20, 
                                          choices=RESERVATION_STATUS, default='pending')
    number_of_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)], 
                                                   default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    cleaning_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    guest_phone = models.CharField(max_length=20, blank=True)
    special_requests = models.TextField(blank=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    is_business_trip = models.BooleanField(default=False)
    guest_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    cancellation_policy = models.CharField(max_length=100, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.guest_name} - {self.property.name} ({self.start_date} to {self.end_date})"

    def get_duration(self):
        return (self.end_date - self.start_date).days

    def calculate_total_price(self):
        duration = self.get_duration()
        return (self.property.price_per_night * duration) + self.cleaning_fee + self.service_fee

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

class MaintenanceTask(models.Model):
    TASK_TYPES = [
        ('cleaning', 'Cleaning'),
        ('laundry', 'Laundry'),
        ('repair', 'Repair'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_tasks')
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_task_type_display()} for {self.property.name} due on {self.due_date}"

    def mark_as_completed(self):
        self.completed = True
        self.save()

class Emergency(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='emergencies')
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "Resolved" if self.resolved_at else "Unresolved"
        return f"{status} emergency at {self.property.name}"

    def resolve(self):
        self.resolved_at = timezone.now()
        self.save()

class PricingRule(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='pricing_rules')
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pricing for {self.property.name} from {self.start_date} to {self.end_date}"

    def save(self, *args, **kwargs):
        if self.start_date > self.end_date:
            raise ValueError("End date must be after start date")
        super().save(*args, **kwargs)

    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_


class Report(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    month = models.DateField()
    occupancy_rate = models.FloatField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()  # JSON or formatted text for detailed report

    def __str__(self):
        return f"Report {self.property.name}"