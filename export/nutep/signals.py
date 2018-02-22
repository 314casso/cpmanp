from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now

from nutep.middleware import get_current_user
from nutep.models import HistoryMeta, UserProfile, Employee
from nutep.services import CRMService, PortalService

from django.contrib.auth.signals import user_logged_in
from nutep.tasks import update_user


def prepare_history(sender, instance, created, **kwargs): 
    if not hasattr(instance, 'user'):
        instance.user = get_current_user()   
    HistoryMeta.objects.create(date=now(), content_object=instance,
                               is_created=created, user=instance.user)


def update_profile(sender, instance, *args, **kwargs):    
    pass 
   
   
def update_employee(sender, instance, *args, **kwargs):
    crm_service = CRMService()
    crm_service.update_employee(instance)                
    portal_service = PortalService()
    portal_service.update_employee(instance)
                     

def private_data(sender, instance, *args, **kwargs):  
    if not instance.owner:
        first_event = instance.first_event()
        if first_event:
            instance.owner = first_event.user
        else:
            instance.owner = get_current_user()


def update_teams(sender, instance, created, **kwargs):
    if created:
        for team in instance.contract.teams.all():             
            instance.teams.add(team)


def do_user_update(sender, user, request, **kwargs):            
    update_user.delay(user)  # @UndefinedVariable
    

def connect_signals():
    user_logged_in.connect(do_user_update)
    pre_save.connect(update_profile, sender=UserProfile)
    pre_save.connect(update_employee, sender=Employee)
