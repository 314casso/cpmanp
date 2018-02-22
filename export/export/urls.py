from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from nutep.views import (RailFreightTrackingAPIView, ReviseAPIView)
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'export.views.home', name='home'),
    # url(r'^export/', include('export.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     url(r'^accounts/login/$', auth_views.login, name='login'),
#     url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += [ 
#     url(r'^$', landing, name='landing'), 
#     url(r'^services/$', ServiceView.as_view(), name='services'),
    url(r'^pingtracking/$', RailFreightTrackingAPIView.as_view(), name='pingtracking'),
    url(r'^pingrevise/$', ReviseAPIView.as_view(), name='pingrevise'),   
]

urlpatterns += [
    url(r'^select2/', include('django_select2.urls')),
]

urlpatterns += [
    url(r'^django-rq/', include('django_rq.urls')),
]

urlpatterns += [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]

from rest_framework import routers
from nutep import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'events', views.EventViewSet, 'events')
router.register(r'trackevents', views.TrackingViewSet, 'trackevents')
router.register(r'reviseevents', views.ReviseViewSet, 'reviseevents')
router.register(r'employees', views.EmployeesViewSet, 'employees')
router.register(r'dealstats', views.DealStats, 'dealstats')
router.register(r'jobstatus', views.JobStatus, 'jobstatus')
router.register(r'news', views.NewsViewSet, 'news')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns 
