# -*- coding: utf-8 -*-
import datetime
import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey,\
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_unicode
from uuslug import slugify
from django.utils.translation import ugettext_lazy as _
import hashlib
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.postgres.fields.array import ArrayField


def base_path(root, filename):    
    from django.conf import settings
    os.umask(0)
    path = u'%s/%s_%s' % (root, datetime.date.today().month, datetime.date.today().year,)
    att_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(att_path):
        os.makedirs(att_path, 0777)    
    return os.path.join(path, slugify(filename, separator="."))


def attachment_path(instance, filename):   
    return base_path('attachments', filename)


def userprofile_path(instance, filename):    
    root = u'profile/%s' % (instance.user,)    
    return base_path(root, filename)


def employee_path(instance, filename):
    hash_object = hashlib.sha1(b'%s' % instance.domainname)    
    root = u'employee/%s' % hash_object.hexdigest()    
    return base_path(root, filename)


class PrivateManager(models.Manager):    
    def for_user(self, user):
        if not user:
            return super(PrivateManager, self).get_queryset().none()
        return super(PrivateManager, self).get_queryset().filter(user=user)
    

class DateQueryEvent(models.Model):
    UNKNOWN = 300    
    PENDING = 100
    SUCCESS = 200
    ERROR = 500
    
    STATUS_CHOICES = (
        (UNKNOWN, u'Не определен'),
        (PENDING, u'В обработке'),
        (SUCCESS, u'Обработано'),
        (ERROR, u'Ошибка'),
    )
    
    
    REVISE = 1    
    TRACKING = 2
    
    TYPE_CHOICES = (
        (REVISE, u'Взаиморасчеты'),
        (TRACKING, u'Слежение'),
    )
    
    date = models.DateTimeField(blank=True, auto_now=True, db_index=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    type = models.IntegerField(choices=TYPE_CHOICES, blank=True, null=True,)
    files = GenericRelation('File')
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNKNOWN)
    note = models.CharField(blank=True, null=True, max_length=255)
    errors = GenericRelation('BaseError')
    company = models.ForeignKey('Company', blank=True, null=True)
    objects = PrivateManager()
    
    def __unicode__(self):
        return u'{0} {1} {2}'.format(self.pk, self.type, self.status)


class Container(models.Model):
    number = models.CharField(max_length=12)
    size = models.CharField(blank=True, null=True, max_length=3)
    type = models.CharField(blank=True, null=True, max_length=10)    
    line = models.CharField(blank=True, null=True, max_length=150)
    def __unicode__(self):
        return u'{0}'.format(self.id)


class Platform(models.Model):
    number = models.CharField(max_length=50)
    foot = models.IntegerField(blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    mtu = models.CharField(max_length=50, blank=True, null=True)


class RailData(models.Model):
    train = models.CharField(max_length=50, blank=True, null=True)
    invoice = models.CharField(max_length=50, blank=True, null=True)
    departurestation = models.CharField(max_length=50, blank=True, null=True)
    departuredate = models.DateField(blank=True, null=True)
    destinationstation = models.CharField(max_length=50, blank=True, null=True)
    totaldistance = models.IntegerField(blank=True, null=True)
    estimatedtime = models.IntegerField(blank=True, null=True)


class RailTracking(models.Model):    
    operationstation = models.CharField(max_length=50, blank=True, null=True)
    daysinroute = models.IntegerField(blank=True, null=True)
    remainingdistance = models.IntegerField(blank=True, null=True)
    arrivaldate = models.DateField(blank=True, null=True)


class FreightData(models.Model):
    bl = models.CharField(max_length=50, blank=True, null=True)
    deal = models.CharField(max_length=50, blank=True, null=True)
    vessel = models.CharField(max_length=50, blank=True, null=True)
    voyage = models.CharField(max_length=50, blank=True, null=True)
    dateoutplan = models.DateField(blank=True, null=True)
    pod = models.CharField(max_length=50, blank=True, null=True)
    podcountry = models.CharField(max_length=50, blank=True, null=True)


class FreightTracking(models.Model):
    departuredate = models.DateField(blank=True, null=True)
    arrivaldate = models.DateField(blank=True, null=True)
    pot = models.CharField(max_length=50, blank=True, null=True)
    arrivaldatepot = models.DateField(blank=True, null=True)
    departuredatepot = models.DateField(blank=True, null=True)
    daysinroute = models.IntegerField(blank=True, null=True)
    arrivaldateactual = models.DateField(blank=True, null=True)


class RailFreightTracking(models.Model):
    event = models.ForeignKey(DateQueryEvent, related_name="tracks")
    container = models.ForeignKey(Container, blank=True, null=True)
    platform = models.ForeignKey(Platform, blank=True, null=True)
    raildata = models.ForeignKey(RailData, blank=True, null=True)
    railtracking = models.ForeignKey(RailTracking, blank=True, null=True)
    freightdata = models.ForeignKey(FreightData, blank=True, null=True)
    freighttracking = models.ForeignKey(FreightTracking, blank=True, null=True)


class File(models.Model):   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(blank=True, null=True, max_length=255)    
    file = models.FileField(upload_to=attachment_path, blank=True, null=True,)
    
    def __unicode__(self):
        return force_unicode(self.title) 


class Team(models.Model):
    name = models.CharField('Наименование', max_length=150, db_index=True)
    users = models.ManyToManyField(User, blank=True, related_name="teams")
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Рабочая группа')
        verbose_name_plural = force_unicode('Рабочие группы')
        ordering = ('name', )        


class Company(models.Model):
    crm_guid = models.CharField(max_length=36, blank=True, null=True)
    ukt_guid = models.CharField(max_length=36, blank=True, null=True)
    name = models.CharField('Наименование', max_length=150, db_index=True)
    members = models.ManyToManyField(User, blank=True, related_name="companies", through='Membership')
    details = JSONField(blank=True, null=True,)
    INN = models.CharField(_('INN'), max_length=14, blank=True, null=True,)   
    KPP = models.CharField(_('KPP'), max_length=10, blank=True, null=True,)    
    logo = models.ImageField(upload_to=userprofile_path, blank=True, null=True,)
    
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('компания')
        verbose_name_plural = force_unicode('компании')
        ordering = ('name', )


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="members")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    
    is_general = models.BooleanField(default=False)
    is_payer = models.BooleanField(default=False)


class BaseModelManager(models.Manager):    
    def get_queryset(self):        
        return super(BaseModelManager, self).get_queryset().filter(deleted=False)


class PrivateModelManager(BaseModelManager):    
    def for_user(self, user):
        if not user:
            return super(PrivateModelManager, self).get_queryset().none()
        return super(PrivateModelManager, self).get_queryset().filter(models.Q(teams__users=user) | models.Q(owner=user)).distinct()


class ProcessDeletedModel(models.Model):    
    _last_event = None
    _first_event = None
    objects = BaseModelManager()
    all_objects = models.Manager()
    deleted = models.BooleanField('Пометка удаления', default=False)    
           
    def last_event(self):
        if not self._last_event:
            if self.history:
                self._last_event = self.history.all().order_by("-date").first()
        return self._last_event
    
    def first_event(self):
        if not self._first_event:
            if self.history:
                self._first_event = self.history.all().order_by("date")[:1].first()
        return self._first_event
    
    class Meta:
        abstract = True 


class PrivateModel(ProcessDeletedModel):
    teams = models.ManyToManyField(Team, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    objects = PrivateModelManager()    
    class Meta:
        abstract = True
    

class HistoryMeta(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')    
    is_created = models.BooleanField(default=False)    
    date = models.DateTimeField(blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)         
    def __unicode__(self):
        return u'{0}'.format(self.user) 
    

class BaseError(models.Model):
    XML = 1
    MODEL = 2
    UNKNOWN = 3 
    WEBFAULT = 4   
    
    TYPE_CHOICES = (
        (XML, force_unicode('Ошибка учетной системы')),
        (WEBFAULT, force_unicode('Ошибка обмена данных')),
        (MODEL, force_unicode('Ошибка данных')),
        (UNKNOWN, force_unicode('Ошибка')),
             
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')   
    date = models.DateTimeField(auto_now_add=True, blank=True)
    code = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    field = models.CharField(max_length=50, db_index=True, blank=True, null=True)            
    message = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=UNKNOWN, db_index=True, blank=True)
    
    def __unicode__(self):
        return u'{0}'.format(self.code) 
    class Meta:
        verbose_name = force_unicode('Ошибка')
        verbose_name_plural = force_unicode('Ошибки')
        ordering = ('id', )


class UserProfile(models.Model):
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)  
    position = models.CharField(_('position'), max_length=150, blank=True)
    user = models.OneToOneField(User, unique=True, related_name='profile')
    valid_till = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to=userprofile_path, blank=True, null=True,)
           
    def get_fullname(self):
        return u'%s %s %s' % (self.user.last_name, self.user.first_name, self.middle_name)    
    
    def __unicode__(self):
        return self.get_fullname()


class Employee(models.Model):
    domainname = models.CharField(max_length=50, unique=True, db_index=True)
    crm_id = models.CharField(max_length=36, blank=True, null=True, unique=True, db_index=True)       
    portal_id = models.IntegerField(blank=True, null=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    job_title = models.CharField(_('job title'), max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=employee_path, blank=True, null=True,)
    head = models.ForeignKey('self', blank=True, null=True)
    mobile = models.CharField(_('mobile'), max_length=20, blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True, null=True,)   
    email = models.EmailField(_('email'), blank=True)
    skype = models.CharField(_('skype'), max_length=20, blank=True, null=True,)  
    users = models.ManyToManyField(User, through='CompanyManager', related_name='managers')  
    
    def fullname(self):
        return u"%s %s %s" % (self.last_name, self.first_name, self.middle_name)    
    
    def __unicode__(self):        
        return u'{0} {1} ({2})'.format(self.first_name, self.last_name, self.domainname)    


class Scope(models.Model):
    name = models.CharField(_('name'), max_length=50)
    
    def __unicode__(self):
        return u'{0}'.format(self.name)
    

class CompanyManager(models.Model):
    employee = models.ForeignKey(Employee, related_name='membership')
    user = models.ForeignKey(User, related_name='membership')
    scope = models.ForeignKey(Scope, blank=True, null=True,)
    
    def __unicode__(self):
        return u"%s is in group %s (as %s)" % (self.employee, self.user, self.scope)


class InfoSource(models.Model):
    name = models.CharField(u'Наименование', max_length=150, db_index=True)
    
    def __unicode__(self):
        return u'{0}'.format(self.name)
    

class News(ProcessDeletedModel):    
    date = models.DateTimeField(db_index=True)
    title = models.CharField(_('title'), max_length=150)
    summary = models.CharField(_('summary'), max_length=250)
    url = models.CharField(_('url'), max_length=250)
    info_source = models.ForeignKey(InfoSource)
    
    class Meta:
        ordering = ('-date', )
    
    def __unicode__(self):
        return u'{0}'.format(self.title)


        