
from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from logyapp import models as cg_models

@admin.register(cg_models.Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('property', 'platform', 'is_active')
    list_filter = ('platform', 'is_active')

@admin.register(cg_models.MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ('property', 'maintenance_type', 'due_date', 'completed')
    list_filter = ('maintenance_type', 'completed')


@admin.register(cg_models.Reservation)
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

@admin.register(cg_models.Property)
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

@admin.register(cg_models.Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('property', 'reported_at', 'resolved_at')
    list_filter = ('resolved_at',)

@admin.register(cg_models.PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date', 'price_per_night')

@admin.register(cg_models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('property', 'month', 'occupancy_rate', 'total_revenue')

@admin.register(cg_models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date', 'commission_rate')

@admin.register(cg_models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active')
    list_filter = ('role', 'is_active')

@admin.register(cg_models.Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date', 'is_available')
    list_filter = ('is_available',)

@admin.register(cg_models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'start_time', 'end_time')

@admin.register(cg_models.ServiceTask)
class ServiceTaskAdmin(admin.ModelAdmin):
    list_display = ('property', 'service_type', 'due_date', 'completed')
    list_filter = ('service_type', 'completed')

@admin.register(cg_models.EmployeeReview)
class EmployeeReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'rating', 'review_date')

@admin.register(cg_models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'amount', 'payment_date', 'is_refund')
    list_filter = ('is_refund',)

@admin.register(cg_models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'rating', 'created_at')