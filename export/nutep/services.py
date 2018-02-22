# -*- coding: utf-8 -*-

from django.core.files.base import ContentFile
from export.local_settings import WEB_SERVISES
from nutep.odata import CRM, Portal
from nutep.models import Employee, DateQueryEvent, Container,\
    RailFreightTracking, Platform, RailData, RailTracking, FreightData,\
    FreightTracking, BaseError
import base64
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client, helpers
from zeep.transports import Transport


class WSDLService(object):
    username = None
    password = None
    url = None
    def __init__(self, settings):
        self.set_client(settings)
            
    def set_client(self, settings):
        for key in settings.iterkeys():             
            setattr(self, key, settings.get(key))   
        
        session = Session()
        session.auth = HTTPBasicAuth(self.username, self.password)         
        self._client = Client(self.url, strict=False, transport=Transport(session=session, timeout=500))  


class DealService(WSDLService):    
    def get_deal_stats(self, user):        
        guids = user.companies.all().values_list('ukt_guid', flat=True)                    
        response = self._client.service.GetDealStats(','.join(guids))                
        return response      


class BaseEventService(WSDLService):
    def log_event_error(self, e, event):
        base_error = BaseError()
        base_error.content_object = event
        base_error.type = BaseError.UNKNOWN
        base_error.message = e
        base_error.save()  
        event.status = DateQueryEvent.ERROR
        event.save()         
    

class ReviseService(BaseEventService):
    def get_revise(self, user, start_date, end_date):
        try:
            event = DateQueryEvent.objects.create(user=user, type=DateQueryEvent.REVISE, status=DateQueryEvent.PENDING)
            company = user.companies.filter(membership__is_payer=True).first()                                 
            if company.ukt_guid:         
                response = self._client.service.GetReport(company.INN, start_date, end_date)
                                   
                if response:
                    file_data = response[0].Data                
                    filename = u'%s-%s.%s' %  (company, 'revise' , 'xlsx')
                    file_store = event.files.create(title=filename)             
                    file_store.file.save(filename, ContentFile(file_data))
                    event.status = DateQueryEvent.SUCCESS                                         
            event.status = DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:            
            self.log_event_error(e, event) 
        
            
class TrackingService(WSDLService):
    def get_track(self, user):
        try:
            event = DateQueryEvent.objects.create(user=user, type=DateQueryEvent.TRACKING, status=DateQueryEvent.PENDING)
            company = user.companies.filter(membership__is_general=True).first()                                 
            if company.ukt_guid:         
                response = self._client.service.GetRailFreightTracking(company.ukt_guid)                   
                if hasattr(response, 'report') and response.report:
                    file_data = response.report[0].data                
                    filename = u'%s-%s.%s' %  (company, 'tracking' , 'xlsx')
                    file_store = event.files.create(title=filename)             
                    file_store.file.save(filename, ContentFile(file_data))
                    event.status = DateQueryEvent.SUCCESS                                           
                if hasattr(response, 'row') and response.row:
                    for datarow in response.row:
                        tracking = RailFreightTracking.objects.create(event=event)
                        mapper = {
                            'container': Container,
                            'platform': Platform,
                            'raildata': RailData,
                            'railtracking': RailTracking,
                            'freightdata': FreightData,
                            'freighttracking': FreightTracking,
                            }
                        for key, model in mapper.items():
                            data_dict = helpers.serialize_object(datarow[key])
                            if data_dict:
                                setattr(tracking, key, model.objects.create(**data_dict))
                        tracking.save()                    
            event.status = DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:            
            self.log_event_error(e, event)                                     
            

class CRMService(object):
    def __init__(self):
        self.odata = CRM(WEB_SERVISES.get('crm'))
    
    def get_user(self, value):
        return self.odata.get_systemuser(value)
    
    def update_employee(self, employee):
        if employee.crm_id:
            return
        user = self.get_user(employee.domainname)
        for k,v in user.items():
            if hasattr(employee, k):
                setattr(employee, k, v)
        if not employee.head:
            print user['parent_crm_id']
            head = self.get_user(user['parent_crm_id'])
            if head:
                obj, created = Employee.objects.get_or_create(domainname=head['domainname'])  # @UnusedVariable
                if obj:
                    employee.head = obj  
        
class PortalService(object):  
    def __init__(self):
        self.odata = Portal(WEB_SERVISES.get('portal'))
    
    def get_user(self, domainname, email):
        return self.odata.get_systemuser(domainname, email)
    
    def update_employee(self, employee):
        if employee.portal_id:
            return        
        user = self.get_user(employee.domainname, employee.email)        
        for k,v in user.items():
            if hasattr(employee, k):
                setattr(employee, k, v)

        if 'imagedata' in user:
            imagedata = user.get('imagedata') 
            if not imagedata:
                return       
            ext = 'jpg'
            imagedata = ContentFile(base64.b64decode(imagedata), name='avatar.' + ext)
            employee.image.save('avatar.jpg', imagedata)           

