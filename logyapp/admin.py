
from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from .models import Property, Listing, Reservation, MaintenanceTask, Emergency, PricingRule, Report

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('property', 'platform', 'is_active')
    list_filter = ('platform', 'is_active')

@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ('property', 'task_type', 'due_date', 'completed')
    list_filter = ('task_type', 'completed')

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('property', 'reported_at', 'resolved_at')

@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date', 'price_per_night')

  
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest_name', 'start_date', 'end_date', 'reservation_status', 'total_price')
    list_filter = ('reservation_status', 'property', 'start_date')
    search_fields = ('guest_name', 'guest_email', 'property__name')
    date_hierarchy = 'start_date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(property__owner=request.user)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('id'),
            'total_revenue': Sum('total_price'),
        }

        response.context_data['summary'] = list(
            qs.values('reservation_status').annotate(**metrics).order_by('reservation_status')
        )

        return response

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'address', 'owner', 'reservation_count', 'total_revenue')
    list_filter = ('type', 'owner')
    search_fields = ('name', 'address')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def reservation_count(self, obj):
        return obj.reservations.all().count()
    reservation_count.short_description = 'Réservations'

    
    # Dans votre méthode ou fonction
    def total_revenue(self, obj):
        total = obj.reservations.aggregate(Sum('total_price'))['total_price__sum']
        formatted_total = f'${total:.2f}' if total else '$0.00'
        return format_html('{}'.format(formatted_total))
    #
    total_revenue.short_description = 'Revenu Total'

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('property', 'month', 'occupancy_rate', 'total_revenue')
    list_filter = ('property', 'month')
    date_hierarchy = 'month'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total_revenue': Sum('total_revenue'),
            'avg_occupancy': Avg('occupancy_rate'),
        }

        response.context_data['summary'] = list(
            qs.values('property__name').annotate(**metrics).order_by('-total_revenue')
        )

        return response
