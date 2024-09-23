from rest_framework import serializers
from logyapp import models as cg_models
from django.utils import timezone

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
    ##id = serializers.CharField(source='pk')
    title = serializers.SerializerMethodField()
    #start = serializers.DateTimeField(source='start_date')
    #end = serializers.DateTimeField(source='end_date')

    start = serializers.SerializerMethodField()  
    end = serializers.SerializerMethodField()
    ## bgColor = serializers.CharField(default='#00a9ff')
    ## color = serializers.CharField(default='white')
    
    def get_start(self, obj):
        return obj.start_date.isoformat()

    def get_end(self, obj):
        return obj.end_date.isoformat()

    def get_title(self, obj):
        return f"Reservation for {obj.property.name}"

    def update(self, instance, validated_data):
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.guest_name = validated_data.get('guest_name', instance.guest_name)
        # Mettez à jour d'autres champs si nécessaire
        instance.save()
        return instance
    
    def to_internal_value(self, data):
        # Si vous avez besoin de faire une validation ou une transformation spécifique
        if 'start_date' in data and isinstance(data['start_date'], str):
            try:
                data['start_date'] = timezone.datetime.fromisoformat(data['start_date'])
            except ValueError:
                raise serializers.ValidationError({"start_date": "Invalid date format. Use ISO format."})

        if 'end_date' in data and isinstance(data['end_date'], str):
            try:
                data['end_date'] = timezone.datetime.fromisoformat(data['end_date'])
            except ValueError:
                raise serializers.ValidationError({"end_date": "Invalid date format. Use ISO format."})

        return super().to_internal_value(data)

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

 
    class Meta:
        model = cg_models.Reservation
        fields = [ 'id', 'title', 'start', 'end', 'guest_name', 'guest_email', 
                  'start_date', 'end_date', 'property',  
                  'reservation_status', 'number_of_guests', 'total_price',
                  ]
        extra_kwargs = {
            'property': {'required': False}  # Rend le champ 'property' optionnel pour les mises à jour
        }
        
        def validate(self, data):
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError("End date must be after start date")
            return data

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

## 
class EmployeeTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.SerializerMethodField()
    start = serializers.DateTimeField(source='due_date')
    end = serializers.DateTimeField(source='due_date')
    description = serializers.CharField()
    status = serializers.CharField()
    task_type = serializers.SerializerMethodField()

    def get_title(self, obj):
        if isinstance(obj, cg_models.MaintenanceTask):
            return f"Maintenance: {obj.get_maintenance_type_display()}"
        elif isinstance(obj, cg_models.ServiceTask):
            return f"Service: {obj.get_service_type_display()}"
        return "Unknown Task"

    def get_task_type(self, obj):
        if isinstance(obj, cg_models.MaintenanceTask):
            return "maintenance"
        elif isinstance(obj, cg_models.ServiceTask):
            return "service"
        return "unknown"
        
###
# serializers.py
class ServiceTaskSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    start = serializers.DateTimeField(source='due_date')
    end = serializers.DateTimeField(source='due_date')

    class Meta:
        model = cg_models.ServiceTask
        fields = ['id', 'title', 'start', 'end', 'description', 'status', 'service_type']

    def get_title(self, obj):
        return f"{obj.get_service_type_display()} - {obj.property.name}"

 