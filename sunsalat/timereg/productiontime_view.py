from django.shortcuts import render, get_object_or_404
from .models import ProductionTime


def production_time_detail(request, production_time_id):
    production_time = get_object_or_404(ProductionTime, id=production_time_id)
    return render(request, 'worktime.html', {'production_time': production_time})