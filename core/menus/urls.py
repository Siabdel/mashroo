#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.5'

from django.conf.urls import url, include
from django.contrib import admin
import views

urlpatterns = [
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/$', views.bookmark_list, name='bookmark_list'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/add/$', views.bookmark_add, name='bookmark_add'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/(?P<slug>[-\w]+)/edit/$', views.bookmark_edit, name='bookmark_edit'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/bookmarks/(?P<slug>[-\w]+)/delete/$', views.bookmark_delete, name='bookmark_delete'),
]
