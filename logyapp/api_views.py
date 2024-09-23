from django.shortcuts import render
from rest_framework import viewsets
# Additional custom views for specific business logic
from rest_framework.views import APIView
from rest_framework.response import Response
from logyapp import models as cg_models
from logyapp import serializes as cg_serializers
import logging
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Reservation, Property, Employee, Task, ServiceTask


logger = logging.getLogger(__name__)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = cg_models.Property.objects.all()
    serializer_class = cg_serializers.PropertySerializer

class ListingViewSet(viewsets.ModelViewSet):
    queryset = cg_models.Listing.objects.all()
    serializer_class = cg_serializers.ListingSerializer

# class baser cet foici sur la class ViewSet et pas la class ModelViewSet
class CustomReservationViewSet(viewsets.ViewSet):
    queryset = cg_models.Reservation.objects.all()  # Ajoutez cette ligne

    def list(self, request):
        reservations = cg_models.Reservation.objects.all()
        calendar_data = {
            'id': 'maintenances',
            'name': 'My Calendar',
            'theme': {},  # Vous pouvez ajouter des configurations de thème ici
            'schedules': reservations
        }
        serializer = cg_serializers.CalendarSerializer(calendar_data)
        return Response([serializer.data])

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = cg_models.Reservation.objects.all()
    serializer_class = cg_serializers.ReservationSerializer
    
    def update(self, request, *args, **kwargs):
        logger.debug(f"Received update data: {request.data}")
        ##
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class MaintenanceTaskViewSet(viewsets.ModelViewSet):
    queryset = cg_models.MaintenanceTask.objects.all()
    serializer_class = cg_serializers.MaintenanceTaskSerializer

class EmergencyViewSet(viewsets.ModelViewSet):
    queryset = cg_models.Emergency.objects.all()
    serializer_class = cg_serializers.EmergencySerializer

class PricingRuleViewSet(viewsets.ModelViewSet):
    queryset = cg_models.PricingRule.objects.all()
    serializer_class = cg_serializers.PricingRuleSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = cg_models.Report.objects.all()
    serializer_class = cg_serializers.ReportSerializer


class OptimizePricingView(APIView):
    def post(self, request, property_id):
        # Logic to optimize pricing based on occupancy and market data
        # This would involve complex calculations and possibly external API calls
        return Response({"message": "Pricing optimized successfully"})

class GenerateMonthlyReportView(APIView):
    def get(self, request, property_id, year, month):
        # Logic to generate and return a monthly report
        # This would aggregate data from various models
        return Response({"report": "Monthly report data"})
## report specifique 
class ReservationCalendarView(APIView):
    def get(self, request):
        property_id = request.query_params.get('property_id')
        city = request.query_params.get('city')
        
        reservations = Reservation.objects.all()
        if property_id:
            reservations = reservations.filter(property_id=property_id)
        if city:
            reservations = reservations.filter(property__city=city)
        
        serializer = cg_serializers.ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class EmployeeTaskCalendarView(APIView):
    def get(self, request):
        employee_id = request.query_params.get('employee_id')
        
        maintenance_tasks = cg_models.MaintenanceTask.objects.all()
        service_tasks = ServiceTask.objects.all()
        
        if employee_id:
            maintenance_tasks = maintenance_tasks.filter(employee_id=employee_id)
            service_tasks = service_tasks.filter(employee_id=employee_id)
        
        all_tasks = list(maintenance_tasks) + list(service_tasks)
        serializer = cg_serializers.EmployeeTaskSerializer(all_tasks, many=True)
        return Response(serializer.data)

# views.py
 
class ServiceTaskCalendarView(APIView):
    def get(self, request):
        service_tasks = ServiceTask.objects.all()
        serializer = cg_serializers.ServiceTaskSerializer(service_tasks, many=True)
        return Response(serializer.data)
