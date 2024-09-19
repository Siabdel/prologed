from django.shortcuts import render, get_object_or_404
from .models import Property, Reservation, Availability

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    availabilities = property.availabilities.filter(is_available=True)
    return render(request, 'property_detail.html', {'property': property, 'availabilities': availabilities})

def reservation_create(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        # Logique de création de réservation
        pass
    return render(request, 'reservation_create.html', {'property': property})
