from django_rq import job
from nutep.services import DealService, TrackingService, ReviseService
from export.local_settings import WEB_SERVISES
import json


@job('default')
def update_user(user):    
    company = user.companies.filter(membership__is_general=True).first()
    if not company:
        return
    deal_service = DealService(WEB_SERVISES['report'])
    deal_stats = deal_service.get_deal_stats(user)    
    company.details = json.loads(deal_stats)
    company.save()
    

@job('default')
def tracking_task(user):            
    service = TrackingService(WEB_SERVISES['report'])                        
    service.get_track(user)
    

@job('default')
def revise_task(user, start_date, end_date):            
    service = ReviseService(WEB_SERVISES['erp'])
    print service.get_revise(user, start_date, end_date)                        
                