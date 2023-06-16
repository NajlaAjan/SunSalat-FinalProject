import datetime
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_related', default=1)
    emp_id = models.CharField(max_length=100, unique=True, blank=True)

    # TODO Der skal trækkes medarbejderid fra Sun Salats database

    def __str__(self):
      return f"{self.user.first_name}" #Tilføj {self.emp_id}

    #TODO Husk at insætte koden til at hente bruger-ID fra det eksterne system
    #response = requests.get('https://api.example.com/employee_id')
        

class ProductionLine(models.Model):
    productionline_name = models.CharField(max_length=100, default='')
    description_text = models.CharField(max_length=200, default='')

    def __str__(self):
        return f"{self.productionline_name}"    


#Registrering af medarbejder ved check in og ud + arbejstid 
class WorkTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worktime_related', default=1)
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)
    completed = models.BooleanField(null=True, default=False) #Ændre null til False

    #Total time spent per check in and out
    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            self.time_spent = self.check_out - self.check_in
        super(WorkTime, self).save(*args, **kwargs)

    def __str__(self):
        formatted_date = str(self.time_spent)
        return f"Work time for {self.user} on {self.production_line} is {formatted_date}"

#    def check_in_employee(self, check_in_time):
#        if not self.check_in and not self.check_out:
#            self.check_in = check_in_time
#            self.save()#
#
#   def check_out_employee(self, check_out_time):
#        if self.check_in and not self.check_out:
#            self.check_out = check_out_time
#            self.save()


#Produktionstid
class ProductionTime(models.Model):
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    #TODO Hent estimeret tid fra Sun salat API
    estimated_production_time = models.DurationField()
    #TODO Gem total tid den 1. i måneden
    actual_production_time = models.DurationField(null=True, blank=True)
    variation_time = models.DurationField(null=True, blank=True)   

    def save(self, *args, **kwargs):
        if self.estimated_production_time and self.actual_production_time:
            self.variation_time = self.actual_production_time - self.estimated_production_time
        super().save(*args, **kwargs)

    def get_variation_time(self):
        return f"Variance time: {self.variation_time}"

    def __str__(self):
        formatted_date = self.date.strftime("%Y-%m-%d Hour: %H:%M:%S")
        return f"Prod. Line: {self.production_line}, Date: {formatted_date} Est. hours spent: {self.estimated_production_time} Actual. hours spent: {self.actual_production_time}"


