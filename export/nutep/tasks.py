import json

from django_rq import job

from export.local_settings import WEB_SERVISES
from nutep.services import AttachedFileService, DealService, OrderService


@job('mosagr')
def update_user(user):    
    company = user.companies.filter(membership__is_general=True).first()
    if not company:
        return
    deal_service = DealService(WEB_SERVISES['report'])
    deal_stats = deal_service.get_deal_stats(user)    
    company.details = json.loads(deal_stats)
    company.save()
    

@job('mosagr')
def pre_order_task(user, start_date):                
    service = OrderService(WEB_SERVISES['cp'])                        
    service.order_list(user, start_date)


def get_attachement(user, guid):
    service = AttachedFileService(WEB_SERVISES['cp'])                        
    file_store = service.get_attachement(user, guid)
    return file_store
