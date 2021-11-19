#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

__author__ = 'Abdelaziz Sadquaoui asadquaoui@strandcosmeticseurope.com'
__copyright__ = 'Copyright (c) 2019 strandcosmeticseurope.fr'
__version__ = '0.9'

from django.conf.urls import url, include
from projects.views import projects as prviews
from projects.views import tickets as tkviews
from django.conf.urls.static import static
from blog.views import ArticleDeleteBlog
from mashroo import settings
import  blog.views as blog_model


urlpatterns =[
    # Projects home

    url(r'^(?P<slug>[-\w]+)/$', blog_model.ArticleHomeBlog.as_view(), name='blog_accueil'),
    url(r'^admin/$', blog_model.ArticleListBlog.as_view(), name='blog_admin'),
    url(r'^show/(?P<pk>[\d]+)/$', blog_model.ArticleDetailBlog.as_view(), name='article_details'),
    url(r'^home/(?P<slug>[-\w]+)/$', blog_model.ArticleHomeBlog.as_view(), name='article_home'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
