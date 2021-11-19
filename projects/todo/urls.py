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
import views

urlpatterns = [
    # Tasks.
    url(r'^tasks/$', views.TaskList.as_view(), name='task_list'),
    url(r'^tasks/unplanned/$', views.unplanned_task_list, name='unplanned_task_list'),
    url(r'^tasks/add/$', views.TaskAdd.as_view(), name='task_add'),
    url(r'^tasks/(?P<pk>\d+)/$', views.TaskDetail.as_view(), name='task_detail'),
    url(r'^tasks/(?P<id>\d+)/edit/$', views.task_edit, name='task_edit'),
    url(r'^tasks/(?P<id>\d+)/delete/$', views.task_delete, name='task_delete'),
    url(r'^tasks/(?P<id>\d+)/close/$', views.task_close, name='task_close'),
    url(r'^tasks/(?P<id>\d+)/reopen/$', views.task_reopen, name='task_reopen'),
]
