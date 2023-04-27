from django.shortcuts import render, get_object_or_404
from ..models import *
from ..forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
import calendar

from ..utils import Calendar
from ..models import *

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'
    
    """ session = request.session.get('login_')
    if session:
        template_name = 'cal/calendar.html'
    else:
        template_name = 'pleaselogin.html' """

    def get_context_data(self, **kwargs):
        # 세션 체크 -> 없으면 로그인플리즈
        session = self.request.session.get('login_')
        """ if not session:
            template = loader.get_template('pleaselogin.html')
            return HttpResponse(template.render({}, self.request))
            global template_name 
            template_name = 'pleaselogin.html'
            return context """
    
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        member = Member.objects.get(email=session)
        categories = Categories.objects.values_list('Cat_name', flat=True)
        context['member'] = member
        context['categories'] = categories
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'cal/event.html', {'form': form})