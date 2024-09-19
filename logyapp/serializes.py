from rest_framework import serializers
from logyapp import models as cg_models

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = cg_models.Listing
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

        
class ReservationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk')
    title = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()  
    end = serializers.SerializerMethodField()
    bgColor = serializers.CharField(default='#00a9ff')
    color = serializers.CharField(default='white')
    
    def get_start(self, obj):
        if obj.check_in_time:
            return f"{obj.start_date}T{obj.check_in_time.isoformat()}"
        return obj.start_date.isoformat()

    def get_end(self, obj):
        if obj.check_out_time:
            return f"{obj.end_date}T{obj.check_out_time.isoformat()}"
        #
        return obj.end_date.isoformat()


    def get_title(self, obj):
        return f"Reservation for {obj.property.name}"

    class Meta:
        model = cg_models.Reservation
        fields = ['id', 'title', 'start', 'end', 'guest_name', 'guest_email', 
                  'reservation_status', 'number_of_guests', 'total_price',
                  'bgColor', 'color', 
                  ]

class PropertySerializer(serializers.ModelSerializer):
    schedules = ReservationSerializer(source='reservations', many=True)

    class Meta:
        model = cg_models.Property
        fields = ['id', 'name', 'schedules']

class CalendarSerializer(serializers.Serializer):
    id = serializers.CharField(default='maintenances')
    name = serializers.CharField(default='My Calendar')
    theme = serializers.DictField(default={})
    schedules = ReservationSerializer(many=True) 