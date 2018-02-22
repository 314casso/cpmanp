# -*- coding: utf-8 -*-

from django import forms
from django.utils.encoding import force_text
from django_select2.forms import ModelSelect2Widget
from nutep.models import UserProfile
from django.forms.forms import Form


class ProfileCustomWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains'        
    ]

    def label_from_instance(self, obj):
        return force_text(u'%s' % (obj.name,))


class ReviseForm(Form):
    action = 'revise'
    form_id = 'reviseFormModal'
    title = u'Запрос ведомости взаиморасчетов'
    ok_title = u'Отправить'
    cancel_title = u'Отмена'
    
    profile = forms.ModelChoiceField(label=u"Плательщик", queryset=UserProfile.objects.all(),
                                      widget=ProfileCustomWidget(
                                          attrs={'style': 'width:100%', 'class': 'form-control', 'required': None}))
    start_date = forms.DateTimeField(label=u"Дата начала", widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))    
    end_date = forms.DateTimeField(label=u"Дата окончания", widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)        
        super(ReviseForm, self).__init__(*args, **kwargs)        
        if user:            
            self.fields['profile'].widget.queryset = user.companies.all()


class TrackingForm(Form):
    action = 'tracking'
    form_id = 'trackingFormModal'
    title = u'Запрос слежения по ЖД и морю'
    ok_title = u'Отправить'
    cancel_title = u'Отмена'
    
    profile = forms.ModelChoiceField(label=u"Клиент", queryset=UserProfile.objects.all(),
                                      widget=ProfileCustomWidget(
                                          attrs={'style': 'width:100%', 'class': 'form-control', 'required': None}))
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)        
        super(TrackingForm, self).__init__(*args, **kwargs)        
        if user:            
            self.fields['profile'].widget.queryset = user.companies.all()
                