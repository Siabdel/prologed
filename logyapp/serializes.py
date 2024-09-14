from rest_framework import serializers
from .models import Property, Listing, Reservation, MaintenanceTask, Emergency, PricingRule, Report

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class MaintenanceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTask
        fields = '__all__'

class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'

class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'