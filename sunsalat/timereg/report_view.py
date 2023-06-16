from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import WorkTime, Employee, ProductionLine, User, ProductionTime
import datetime
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.core import serializers
import logging
from django.contrib.admin.views.decorators import staff_member_required
from chartkick.django import PieChart, LineChart, ColumnChart
import chartkick



logger = logging.getLogger(__name__)

def dashboard(request):
    return render(request, 'dashboard.html')

def charts(request):
    timefmt = '%M'
    formatted_startdate = datetime.datetime.now().date() - datetime.timedelta(days=1)
    formatted_enddate = datetime.datetime.now().date() + datetime.timedelta(days=1)
    result = list(WorkTime.objects.filter(check_in__gte=formatted_startdate, check_in__lte=formatted_enddate).values('production_line').order_by('production_line').annotate(total_timespent=Sum('time_spent')))
    chart_data = {}
    for line in result:
        at_spent_secs =  (line['total_timespent']).total_seconds()
        at_spent_secs = datetime.datetime.utcfromtimestamp(at_spent_secs)
        line['total_timespent'] = at_spent_secs.strftime(timefmt)
        chart_data.update({line['production_line']:line['total_timespent']})
    chart = ColumnChart(chart_data)
    return render(request, 'charts.html', {'chart': chart})

@staff_member_required
@requires_csrf_token
@csrf_protect
def prod_line_report(request):
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'):
        startdate = request.POST.get('startdate', None) 
        enddate = request.POST.get('enddate', None) 
       #if date: #cheking if first_name and last_name have value
        results = get_time_spent(startdate, enddate)
        response = {
                    'msg': results # response message
                    }
        return JsonResponse(response) # return response as JSON 
    return render(request, 'prod_line_report.html')

#Total hours by production lines
def get_time_spent(startdate, enddate):
    datefmt = '%Y-%m-%d'
    timefmt = '%H:%M:%S'
    formatted_startdate = datetime.datetime.strptime(startdate, datefmt).date()
    formatted_enddate = datetime.datetime.strptime(enddate, datefmt).date() + datetime.timedelta(days=1)
    result = list(WorkTime.objects.filter(check_in__gte=formatted_startdate, check_in__lte=(formatted_enddate)).values('production_line').order_by('production_line').annotate(total_timespent=Sum('time_spent')))
    for line in result:
        prod_time_results = list(ProductionTime.objects.filter(production_line = line['production_line'], date=formatted_startdate).values('estimated_production_time'))
        at_spent = datetime.datetime.utcfromtimestamp((line['total_timespent']).total_seconds())
        at_spent_secs = (line['total_timespent']).total_seconds()
        line['total_timespent'] = at_spent.strftime(timefmt)
        for time in prod_time_results:
            est_spent = datetime.datetime.utcfromtimestamp((time['estimated_production_time']).total_seconds())
            est_spent_secs = (time['estimated_production_time']).total_seconds()
            line['variance'] = (((at_spent_secs - est_spent_secs) / at_spent_secs) * 100).__round__(2).__str__() + '%'
            line['estimated_production_time'] = est_spent.strftime(timefmt)
    return result

@staff_member_required
@requires_csrf_token
@csrf_protect
def pline_emp_report(request):
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'):
        startdate = request.POST.get('startdate', None) 
        enddate = request.POST.get('enddate', None) 
        pline = request.POST.get('pline', None)
        results = emp_ts_pline(startdate, enddate, pline)
        response = {
                    'msg': results # response message
                    }
        return JsonResponse(response) # return response as JSON 
    return render(request, 'pline_emp_report.html')


#Total employee hours by productions line - tts(total time spent)
def emp_ts_pline(startdate, enddate, pline):
    formatted_startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d').date()
    formatted_enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d').date()
    if pline == '':
        result = list(WorkTime.objects.filter(check_in__gte=formatted_startdate, check_in__lte=formatted_enddate).values('user').order_by('user').annotate(total_timespent=Sum('time_spent')))
    else:
        result = list(WorkTime.objects.filter(check_in__gte=formatted_startdate, check_in__lte=formatted_enddate, production_line=pline).values('user').order_by('user').annotate(total_timespent=Sum('time_spent')))
    for line in result:
        tt_spent = datetime.utcfromtimestamp((line['total_timespent']).total_seconds())
        line['total_timespent'] = tt_spent.strftime('%H:%M:%S')
        user = User.objects.get(pk = line['user'])
        line['user'] = user.first_name + " " + user.last_name
    return result

@staff_member_required
@requires_csrf_token
@csrf_protect
def emp_report(request):
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'):
        startdate = request.POST.get('startdate', None) 
        enddate = request.POST.get('enddate', None) 
       #
        results = emp_ts(startdate, enddate)
        response = {
                    'msg': results # response message
                    }
        return JsonResponse(response) # return response as JSON 
    return render(request, 'emp_report.html')
    

#Antal timer pr. medarbejder pr. produktionslinje - tts(total time spent)
def emp_ts(startdate, enddate):
    formatted_startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d').date()
    formatted_enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d').date()
    result = list(WorkTime.objects.filter(check_in__gte=formatted_startdate, check_in__lte=formatted_enddate).values('user').order_by('user').annotate(total_timespent=Sum('time_spent')))
    for line in result:
        tt_spent = datetime.datetime.utcfromtimestamp((line['total_timespent']).total_seconds())
        line['total_timespent'] = tt_spent.strftime('%H:%M')
        user = User.objects.get(pk = line['user'])
        line['user'] = user.first_name + " " + user.last_name
    return result