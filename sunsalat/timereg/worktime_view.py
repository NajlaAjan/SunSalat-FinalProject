
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import WorkTime, Employee, ProductionLine
from datetime import datetime, timezone
from django.contrib.auth import logout


def index(request, pline):
    if not pline:
        pline = 1        
    return render(request, 'worktime.html', {'pline': pline})

@login_required
def checkin(request, pline):
    productionline = ProductionLine.objects.get(id=pline)
    now = datetime.now(timezone.utc)
    current_user = request.user
    InProgress = WorkTime.objects.filter(user_id=current_user.id, production_line=pline, completed=False)

    if (InProgress):
        request.session['message'] = 'You already checked-in!'
        request.session.set_expiry(5) 
        return redirect('worktime', pline=pline)

    else:  
        timeentry = WorkTime.objects.create(check_in=now,production_line = productionline, user = current_user)
        timeentry.save()
        request.session['message'] = 'Check-in successful!'
        request.session.set_expiry(5) 
        return redirect('worktime', pline=pline)


@login_required
def checkout(request, pline):
    current_user = request.user
    now = datetime.now(timezone.utc)
    InProgress = WorkTime.objects.filter(user_id=current_user.id, production_line=pline, completed=False)
    if not (InProgress):
        request.session['message'] = 'You already checked-out!'
        return redirect('worktime', pline=pline)
    timeentrylist = WorkTime.objects.filter(user_id=current_user.id, production_line=pline, completed=False).order_by("check_in")
    timeentry = timeentrylist.first()
    timeentry.check_out=now
    timeentry.completed=True
    timeentry.save()
    #find employee_id
    #Find seneste tidsentry i worktime tabellen
    request.session['message'] = 'Check-out successful!'
    request.session.set_expiry(5) 
    return redirect('worktime', pline=pline)
    


