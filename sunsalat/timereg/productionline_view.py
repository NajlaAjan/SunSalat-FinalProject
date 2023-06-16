
from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductionLine
from django.http import HttpResponse

#production line overview for epmloyee page
def production_line_list(request):
    production_lines = ProductionLine.objects.all()
    for productionline in production_lines:
        ProductionLine.productionline_name
    return render(request, 'productionline.html', {'production_lines': production_lines})

