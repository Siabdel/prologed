
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet)
router.register(r'listings', views.ListingViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'maintenance-tasks', views.MaintenanceTaskViewSet)
router.register(r'emergencies', views.EmergencyViewSet)
router.register(r'pricing-rules', views.PricingRuleViewSet)
router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('optimize-pricing/<int:property_id>/', views.OptimizePricingView.as_view(), name='optimize-pricing'),
    path('generate-report/<int:property_id>/<int:year>/<int:month>/', views.GenerateMonthlyReportView.as_view(), name='generate-report'),
]