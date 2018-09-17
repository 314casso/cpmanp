from django.contrib.auth.models import User
from rest_framework import serializers
from nutep.models import DateQueryEvent, File, UserProfile,\
    Container,Employee, PreOrder, CustomsProcedure, ProcedureLog


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('middle_name', 'position')
    

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'profile')
        

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('title', 'file', 'guid', 'storage', 'id')


class ProcedureLogProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureLog
        fields = '__all__'


class CustomsProcedureSerializer(serializers.ModelSerializer):
    logs = ProcedureLogProcedureSerializer(many=True)
    class Meta:
        model = CustomsProcedure
        fields = '__all__'


# class FilteredListSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         user = self.context['request'].user
#         company = user.companies.filter(membership__is_general=True).first()        
#         membership = user.members.get(company=company)
#         if membership.is_restricted:            
#             data = data.filter(payerguid=company.payer_guid)
        
#         return super(FilteredListSerializer, self).to_representation(data)


class ContainerSerializer(serializers.ModelSerializer):
    procedures = CustomsProcedureSerializer(many=True)
    files = FileSerializer(many=True)
    class Meta:
        # list_serializer_class = FilteredListSerializer
        model = Container
        fields = '__all__'


class EventStatusSerializer(serializers.ModelSerializer):       
    # user = UserSerializer()  
    class Meta:
        depth = 1
        model = DateQueryEvent
        fields = ('id', 'date', 'type', 'status')


class PreOrderSerializer(serializers.ModelSerializer):
    event = EventStatusSerializer()
    containers = ContainerSerializer(many=True, read_only=True)    
    class Meta:
        model = PreOrder        
        fields = '__all__'


class EmployeesSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        depth = 1
        model = Employee
        fields = ('domainname','crm_id','portal_id','first_name','last_name','middle_name','job_title','image','head','mobile','phone','email','skype','users')
             


        