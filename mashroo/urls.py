"""mashroo URL Configuration

The `pathpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to pathpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.paths import include, path
    2. Add a URL to pathpatterns:  path('blog/', include('blog.urls'))
"""
import datetime
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from rest_framework import routers
from django.contrib import admin
# from mashroo.projects.utils import export_as_json, export_as_cvs
# import notifications.paths



urlpatterns = [
    path(r'', TemplateView.as_view(template_name="siteweb/index.html"), kwargs={'semaine': datetime.datetime.now().isocalendar()[1] }),
    # app admin
    path(r'admin/', admin.site.urls),
    # path(r'^api/', include('routers.urls')),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),

    path(r'account/',   include('allauth.urls')),
    # markdown editor
    path(r'mdeditor/' , include('mdeditor.urls' )),
    # taxonomie methode de classification de l'information (search , categories, tags)path(r'^do/', include('todo.urls')),
    path(r'taxo/',  include('core.taxonomy.urls')),
    path(r'do/',    include('todo.urls')),
    path(r'pro/',   include('projects.urls')),
    path('avatar/', include('avatar.urls')), # avatar

    #  notifications django-notify-x
    path(r'notifications/', include('notify.urls', 'notifications')),
    #  blog
    path(r'blog/admin/', include('blog.urls_admin')),
    path(r'blog/', include('blog.urls')),


    # export data
    # path(r'api/get_of/(?P<filtre>[\w]{1,3})/(?P<semaine>[\d]{2})/(?P<annee>[\d]{2,4})/$',  api_get_ofs,  name='api_get_of' ),
    # http://localhost:8000/export/?ct=26&ids=353905,340433
    # path(r'export/json/(?P<ct>[\d]+)/(?P<ids>[\w,]+)/$', "mashroo.projects.utils.export_as_json"),
    # path(r'export/csv/(?P<ct>[\d]+)/(?P<ids>[\w,]+)/$', export_as_cvs),
    ]



if settings.DEBUG:
    import debug_toolbar
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]
