# -*- coding: utf-8 -*-

from __future__ import division

import datetime
import json
import logging
from datetime import timedelta

import django_rq
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from nutep.forms import ReviseForm, TrackingForm
from nutep.models import Company, DateQueryEvent, PreOrder
from nutep.serializers import EmployeesSerializer, EventStatusSerializer, \
    PreOrderSerializer, UserSerializer
from nutep.tasks import pre_order_task


logger = logging.getLogger('django.request')


class DeleteMixin(SingleObjectMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteMixin, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user = self.request.user
        self.object.deleted = True
        self.object.save()
        return HttpResponse(json.dumps({'pk': self.object.id}), content_type="application/json")


class BaseView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)
    
    def get_company(self):
        return self.request.user.companies.filter(membership__is_general=True).first()
        
    def get_dealstats(self, dateformat="%d.%m.%Y %H:%M:%S"):
        company = self.request.user.companies.filter(membership__is_general=True).first()
        if not company:
            return
        deal_stats = company.details.get('DealStats')
        if deal_stats:
            result = {}
            result['dealdate'] = datetime.datetime.strptime(deal_stats.get('FirstDeal'), dateformat)
            result['totaldeals'] = deal_stats.get('TotalDeals')
            result['lastmonth'] = deal_stats.get('LastMonth')
            result['days_together'] = (datetime.datetime.now() - result['dealdate']).days            
            return result

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        manager = self.request.user.managers.first()
        head = None
        if manager:
            manager.title = u"Ваш менеджер"            
            head = manager.head
            if head:
                head.title = u"Руководитель менеджера"
        
        start_date = datetime.date.today().replace(day=1)
        revise_form = ReviseForm(user=self.request.user, initial={'start_date': start_date.strftime('%d.%m.%Y')})
        tracking_form = TrackingForm(user=self.request.user)
                
        context.update({
            'title': force_unicode('МАНП Онлайн'), 
            'manager': manager,
            'head': head,            
            'company': self.get_company(),
        })         
        return context


def landing(request):    
    if request.user.is_authenticated():
        company = request.user.companies.filter(membership__is_general=True).first()        
        if company:
            return redirect(company.get_dashboard_url())                    
        return redirect(Company.DASHBOARD_VIEW)
    else:
        return redirect('login')


class ServiceView(BaseView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        context.update({
            'title': force_unicode('Рускон Онлайн'),        
        })
        return context


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

 
class PingOrderList(viewsets.ViewSet):
    def list(self, request):
        today = now()
        key = 'last_ping_order_list'
        if cache.get(key):
            return Response({ 'job': 'cached' })
        cache.set(key, today, 300)   
        start_date = today - timedelta(days=360)
        job = pre_order_task.delay(request.user, start_date)  # @UndefinedVariable        
        return Response({ 'job': job.id })  
 
  
class JobStatus(viewsets.ViewSet):
    def retrieve(self, request, pk):       
        queue = django_rq.get_queue('mosagr')
        job = queue.fetch_job(pk)
        status = job.status if job else None
        return Response({ 'job': status })
    

class EventViewSet(viewsets.ModelViewSet):    
    serializer_class = EventStatusSerializer
    def get_queryset(self):
        DateQueryEvent.objects.for_user(self.request.user).filter(status__in=(DateQueryEvent.ERROR, DateQueryEvent.PENDING)).order_by('-date')        
    

class EmployeesViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeesSerializer
    def get_queryset(self):
        return self.request.user.managers.all()    
          
                      
class OrderListViewSet(viewsets.ModelViewSet):
    serializer_class = PreOrderSerializer                         
    def get_queryset(self):
        event = DateQueryEvent.objects.for_user(self.request.user).filter(status=DateQueryEvent.SUCCESS).order_by('-date').first()
        if not event:
            return PreOrder.objects.none()        
        return event.orders.filter(containertrain__isnull=False).order_by('date')
                          