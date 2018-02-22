# -*- coding: utf-8 -*-
import requests
from requests_ntlm import HttpNtlmAuth
import urlparse

class BaseSession(object):
    session = None
    def __init__(self, settings):         
        self.url = settings['url']
        self.set_session(settings['username'], settings['password'])
        
    def make_url(self, url):
        return urlparse.urljoin(self.url, url)    
        
    def set_session(self, username, password):
        if not self.session:        
            session = requests.Session()
            session.auth = HttpNtlmAuth(username, password, session)
            self.session = session
       

class CRM(BaseSession):
    def get_systemuser(self, value):
        if not value:
            return
        if not value.find('\\') == -1: 
            url = self.make_url("systemusers?$filter=domainname eq '%s'" % value)
        else:
            url = self.make_url("systemusers?$filter=systemuserid eq %s" % value)
        r = self.session.get(url)
        try:
            data = r.json()
        except ValueError:            
            return
        if not 'value' in data:
            return
        user = data['value'][0]
        dto = {
             'domainname': user['domainname'],
             'crm_id' : user['systemuserid'],                     
             'first_name' : user['firstname'],
             'last_name' : user['lastname'],
             'middle_name' : user['middlename'],
             'job_title' : user['jobtitle'],
             'email' : user['internalemailaddress'],
             'parent_crm_id': user['_parentsystemuserid_value']
        }
        return dto    


class Portal(BaseSession):
    def get_systemuser(self, domainname, email):
        domain, login = domainname.split("\\")                 
        url = self.make_url('get_user.php')
        self.session.get(url)      
        r = self.session.post(url, data={'LOGIN': login, 'EXTERNAL_AUTH_ID': domain.upper(), 'EMAIL': email})
        if not r.status_code == 200:
            return
        try:
            data = r.json()
        except ValueError:            
            return
        if len(data) == 1:
            user = data[0]            
            dto = {
            'portal_id' : user['ID'],                                       
            'mobile' : user['PERSONAL_MOBILE'],             
            'imagedata' : user['image'],        
            # 'first_name' : user['NAME'],
            # 'last_name' : user['LAST_NAME'],
            # 'middle_name' : user['SECOND_NAME'],
            # 'job_title' : user['WORK_POSITION'],
             } 
            return dto



