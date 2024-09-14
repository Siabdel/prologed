from django import forms
from .models import Property, Listing, Reservation, MaintenanceTask, Emergency, PricingRule

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'type', 'address', 'owner']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['property', 'platform', 'listing_url', 'is_active']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['property', 'start_date', 'end_date', 'guest_name', 'guest_email']

class MaintenanceTaskForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ['property', 'task_type', 'description', 'due_date']

class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['property', 'description']

class PricingRuleForm(forms.ModelForm):
    class Meta:
        model = PricingRule
        fields = ['property', 'start_date', 'end_date', 'price_per_night']