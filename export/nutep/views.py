# -*- coding: utf-8 -*-

from __future__ import division

import datetime
import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
import django_rq

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from nutep.forms import ReviseForm, TrackingForm
from nutep.models import News, DateQueryEvent
from nutep.serializers import UserSerializer, DateQueryTrackingSerializer, \
    EventStatusSerializer, DateQueryReviseSerializer, EmployeesSerializer,\
    NewsSerializer
from nutep.tasks import tracking_task, revise_task
from django.utils.timezone import now
from datetime import timedelta


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
    
    def news(self):        
        limit = 5
        return News.objects.all()[:limit]
    
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
        
        dealstats = self.get_dealstats()
        
        start_date = datetime.date.today().replace(day=1)
        revise_form = ReviseForm(user=self.request.user, initial={'start_date': start_date.strftime('%d.%m.%Y')})
        tracking_form = TrackingForm(user=self.request.user)
                
        context.update({
            'title': force_unicode('Рускон Онлайн'), 
            'manager': manager,
            'head': head,
            'news': self.news(),
            'dealstats': dealstats,
            'revise_form': revise_form,
            'tracking_form': tracking_form,
        })         
        return context


def landing(request):
    if request.user.is_authenticated():
        return redirect('services')
    context = {
        'title': force_unicode('Рускон'),
    }
    return render(request, 'landing.html', context)


class ServiceView(BaseView):
    template_name = 'base.html'

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


class TrackingViewSet(viewsets.ModelViewSet):     
    serializer_class = DateQueryTrackingSerializer
    def get_queryset(self):
        return DateQueryEvent.objects.for_user(self.request.user).filter(type=DateQueryEvent.TRACKING).order_by('-date')[:1]
 
 
class ReviseViewSet(viewsets.ModelViewSet):
    serializer_class = DateQueryReviseSerializer
    def get_queryset(self):
        return DateQueryEvent.objects.for_user(self.request.user).filter(type=DateQueryEvent.REVISE).order_by('-date')[:1]
 
 
class RailFreightTrackingAPIView(APIView):
    def post(self, request):
        job = tracking_task.delay(request.user)  # @UndefinedVariable        
        return Response({ 'job': job.id })
    
    
class ReviseAPIView(APIView):
    def post(self, request):
        today = now()
        start_date = today - timedelta(days=360) 
        end_date = today
        job = revise_task.delay(request.user, start_date, end_date)  # @UndefinedVariable        
        return Response({ 'job': job.id })    


class JobStatus(viewsets.ViewSet):
    def retrieve(self, request, pk):        
        print request.POST       
        queue = django_rq.get_queue('default')
        job = queue.fetch_job(pk)
        status = job.status if job else None
        return Response({ 'job': status })
    

class DealStats(viewsets.ViewSet):
    def list(self, request):       
        company = request.user.companies.filter(membership__is_general=True).first()
        if not company:
            return Response({})
        deal_stats = company.details.get('DealStats')
        if deal_stats:
            return Response({ 'deal_stats': deal_stats })
        return Response({})    
    

class EventViewSet(viewsets.ModelViewSet):    
    serializer_class = EventStatusSerializer
    def get_queryset(self):
        DateQueryEvent.objects.for_user(self.request.user).filter(status__in=(DateQueryEvent.ERROR, DateQueryEvent.PENDING)).order_by('-date')        
    

class EmployeesViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeesSerializer
    def get_queryset(self):
        return self.request.user.managers.all()    


class NewsViewSet(viewsets.ModelViewSet):
    limit = 5
    serializer_class = NewsSerializer
    def get_queryset(self):        
        return News.objects.all()[:self.limit]                          
                          
                          
