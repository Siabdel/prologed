from rest_framework import serializers
from logyapp import models as cg_models

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Property
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Listing
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Reservation
        fields = '__all__'

class MaintenanceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.MaintenanceTask
        fields = '__all__'

class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Emergency
        fields = '__all__'

class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.PricingRule
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Report
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Contract
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Employee
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Availability
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Schedule
        fields = '__all__'

class ServiceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.ServiceTask
        fields = '__all__'

class EmployeeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.EmployeeReview
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Payment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Review
        fields = '__all__'