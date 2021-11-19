import datetime
from django.views.generic import TemplateView
from django.conf.urls import include, url
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
from ofschedule.views import export_as_json, export_as_cvs
# import notifications.urls

admin.autodiscover()

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name="homepage.html"),),
    url(r'^$', TemplateView.as_view(template_name="projects/index.html"), kwargs={'semaine': datetime.datetime.now().isocalendar()[1],
                                                                                  'annee': unicode(datetime.datetime.now().year)[:-2] ,
                                                                                   }),

    # app admin
    url(r'^admin/', admin.site.urls),
    # url(r'^api/', include('routers.urls')),
    #   url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))

    url(r'^account/',   include('allauth.urls')),
    url(r'^accounts/',  include('allauth.urls')),

    url(r'^schedule/', include('schedule.urls')),
    # module planning OF
    url(r'^of/', include('ofschedule.urls')),
    # module demande approviews
    url(r'^da/', include('approvisionnement.urls')),
    # module OF
    url(r'^ofsce/', include('of_module.urls')),
    # module business data
    url(r'^bi/', include('businessce.urls')),
    # project todo
    # taxonomie methode de classification de l'information (search , categories, tags)url(r'^do/', include('todo.urls')),
    url(r'^taxo/',  include('core.taxonomy.urls')),
    url(r'^do/',    include('todo.urls')),
    url(r'^pro/',   include('projects.urls')),
    url('avatar/', include('avatar.urls')), # avatar
    #  notifications django-notify-x
    url(r'^notifications/', include('notify.urls', 'notifications')),


    # export data
    # url(r'^api/get_of/(?P<filtre>[\w]{1,3})/(?P<semaine>[\d]{2})/(?P<annee>[\d]{2,4})/$',  api_get_ofs,  name='api_get_of' ),
    # http://localhost:8000/export/?ct=26&ids=353905,340433
    url(r'^export/json/(?P<ct>[\d]+)/(?P<ids>[\w,]+)/$', export_as_json),
    url(r'^export/csv/(?P<ct>[\d]+)/(?P<ids>[\w,]+)/$', export_as_cvs),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
