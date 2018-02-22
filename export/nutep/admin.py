# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from nutep.models import (BaseError, UserProfile, Team, CompanyManager,
    Employee, News, InfoSource, File, Company, Membership, DateQueryEvent,
    Container, RailFreightTracking)
from nutep.services import DealService
from export.local_settings import WEB_SERVISES
import json
from django.contrib.contenttypes.admin import GenericTabularInline

admin.site.unregister(User)


class ManagerInline(admin.TabularInline):
    model = CompanyManager  # @UndefinedVariable
    extra = 1


class UserProfileInline(admin.StackedInline):
    model = UserProfile  
    

class FileAdmin(admin.ModelAdmin):
    pass
    

class FileInline(GenericTabularInline):
    model = File  # @UndefinedVariable
    extra = 1
    
    
class CompanyInline(admin.TabularInline):
    model = Membership  # @UndefinedVariable
    extra = 1
        
    
class TeamInline(admin.TabularInline):
    model = Team.users.through  # @UndefinedVariable
    extra = 1


class UserProfileAdmin(UserAdmin):    
    inlines = [UserProfileInline, CompanyInline, TeamInline, ManagerInline, FileInline]
    
    actions = ['get_deal_stats']
    
    def get_deal_stats(self, request, queryset):
        for user in queryset:            
            deal_service = DealService(WEB_SERVISES['report'])
            deal_stats = deal_service.get_deal_stats(user)
            user.profile.details = json.loads(deal_stats)
            user.profile.save() 
            
    get_deal_stats.short_description = u"Обновить статистику"    


class TeamAdmin(admin.ModelAdmin):  
    pass


class CompanyAdmin(admin.ModelAdmin):  
    pass


class EmployeeAdmin(admin.ModelAdmin):
    pass


class NewsAdmin(admin.ModelAdmin):
    list_display = ['date', 'title']


class InfoSourceAdmin(admin.ModelAdmin):
    pass


class ErrorInline(GenericTabularInline):
    model = BaseError  # @UndefinedVariable
    extra = 0


class DateQueryEventAdmin(admin.ModelAdmin):
    inlines = [ErrorInline, FileInline]


class ContainerAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserProfileAdmin)
admin.site.register(BaseError)
admin.site.register(Team, TeamAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(InfoSource, InfoSourceAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(DateQueryEvent, DateQueryEventAdmin)
admin.site.register(Container, ContainerAdmin)
admin.site.register(RailFreightTracking)

