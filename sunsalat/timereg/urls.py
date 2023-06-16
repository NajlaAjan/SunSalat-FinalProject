from django.urls import path
from . import productionline_view, worktime_view, report_view, productiontime_view
from django.contrib.auth import views as auth_views
from django.urls import include


urlpatterns = [
    path('', report_view.dashboard, name='dashboard'),
    path("productionlinelist/", productionline_view.production_line_list, name="production_line_list"),
    path("worktime/<int:pline>/", worktime_view.index, name="worktime"),
    path('worktime/checkin/<int:pline>/', worktime_view.checkin, name="checkin"),
    path('worktime/checkout/<int:pline>/', worktime_view.checkout, name="checkout"),
    path('prodlinereport/', report_view.prod_line_report, name='prod_line_report'),
    path('pline-empreport/', report_view.pline_emp_report, name='pline_emp_report'),
    path('empreport/', report_view.emp_report, name='emp_report'),
    path('charts/', report_view.charts, name='charts'),
    

] 