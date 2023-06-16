from django.contrib import admin
from .models import Employee, ProductionLine, ProductionTime, WorkTime


# models.
admin.site.register(Employee)
admin.site.register(ProductionLine)
admin.site.register(ProductionTime)
admin.site.register(WorkTime)


