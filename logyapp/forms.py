from django import forms
from .models import Property, Listing, Reservation, MaintenanceTask, Emergency, PricingRule
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Reservation, Property

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['property', 'start_date', 'end_date', 'guest_name', 'guest_email']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('property', css_class='form-group col-md-6 mb-0'),
                Column('guest_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'guest_email',
            Submit('submit', 'Réserver', css_class='btn btn-primary')
        )

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'type', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'type',
            'address',
            Submit('submit', 'Enregistrer', css_class='btn btn-success')
        )

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['property', 'platform', 'listing_url', 'is_active']


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