from django_rq import job
from nutep.services import DealService, OrderService
from export.local_settings import WEB_SERVISES
import json
from time import sleep


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
def pre_order_task(user, start_date):                
    service = OrderService(WEB_SERVISES['cp'])                        
    service.order_list(user, start_date)
    
                        
                