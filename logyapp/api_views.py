from django.shortcuts import render
from rest_framework import viewsets
# Additional custom views for specific business logic
from rest_framework.views import APIView
from rest_framework.response import Response
from logyapp import models as cg_models
from logyapp import serializes as cg_serializers

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


