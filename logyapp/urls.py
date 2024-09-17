
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from logyapp import views as cg_views
from logyapp import api_views as api_views
  

router = DefaultRouter()
router.register(r'properties', api_views.PropertyViewSet)
router.register(r'listings', api_views.ListingViewSet)
router.register(r'reservations', api_views.ReservationViewSet)
router.register(r'maintenance-tasks', api_views.MaintenanceTaskViewSet)
router.register(r'emergencies', api_views.EmergencyViewSet)
router.register(r'pricing-rules', api_views.PricingRuleViewSet)
router.register(r'reports', api_views.ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('optimize-pricing/<int:property_id>/', api_views.OptimizePricingView.as_view(), name='optimize-pricing'),
    path('generate-report/<int:property_id>/<int:year>/<int:month>/', api_views.GenerateMonthlyReportView.as_view(), name='generate-report'),
]