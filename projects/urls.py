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
# API
from rest_framework.urlpatterns import format_suffix_patterns
from mashroo import settings
from django.conf.urls.static import static
from core.profile import models as profilmodel
from businessce import views as businessviews

urlpatterns =[
    # Projects home

    url(r'^projects/$', prviews.ProjectHomeView.as_view(), name='project_home'),
    url(r'^lastprojects/(?P<filtre>[\w]+)/$', prviews.ProjectHomeViewFiltre.as_view(), name='project_home'),

    # Projects.
    url(r'^projects/list/$', prviews.ProjectListView.as_view(), name='project_list'),
    url(r'^projects/add/$', prviews.ProjectCreateView.as_view(), name='project_add'),
    url(r'^projects/(?P<pk>[\d]+)/$', prviews.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^projects/(?P<pk>[-\d]+)/edit/$',     prviews.ProjectEditView.as_view(), name='project_edit'),
    url(r'^projects/(?P<pk>[-\d]+)/delete/$',   prviews.ProjectDeleteView.as_view(),  name='project_delete'),
    # project_timeline'
    url(r'^projects/(?P<pk>[-\d]+)/timeline/$',   prviews.ProjectDetailView.as_view(), {'template_name': 'projects/project_timeline.html'}, name='project_timeline'),

    # Tickets.
    url(r'^projects/(?P<project_id>[-\w]+)/tickets/$',  tkviews.TicketListView.as_view(), name='ticket_list'),
    url(r'^mestickets/(?P<user_id>[-\d]+)/$',  tkviews.MyTicketsListView.as_view(), name='mes_ticket_list'),

    url(r'^projects/(?P<project_id>[-\d]+)/tickets/add/$', tkviews.TicketAddView.as_view(), name='ticket_add'),

    url(r'^projects/tickets/(?P<pk>\d+)/$', tkviews.TicketDetailView.as_view(), name='ticket_detail'),
    url(r'^projects/tickets/(?P<pk>\d+)/edit/$', tkviews.TicketEditView.as_view(), name='ticket_edit'),

    url(r'^projects/(?P<project_id>[-\w]+)/tickets/(?P<code>\d+)/delete/$', tkviews.TicketDeleteView, name='ticket_delete'),

    # ticket tasks
    url(r'^projects/(?P<project_id>[-\w]+)/tickets/(?P<code>\d+)/tasks/$', tkviews.ticket_detail , {'template_name': 'projects/ticket_tasks.html'}, 'ticket_tasks'),
    url(r'^projects/(?P<project_id>[-\w]+)/tickets/(?P<code>\d+)/timeline/$', tkviews.ticket_detail , {'template_name': 'projects/ticket_timeline.html'}, 'ticket_timeline'),

    # todo simple
    url(r'^todo/$', prviews.todo_today,   name='todo_today'),

    # boite reception
    url(r'^notification/$', prviews.notification_list,   name='notification_url'),

    # profile user
    url(r'^profile/(?P<user_id>[-\d]+)/$', prviews.MyProfileDetailView.as_view(),   name='profile_user'),
    url(r'^profile/(?P<user_id>[-\d]+)/edit/$', prviews.MyProfileEditView.as_view(),   name='profile_user_edit'),

    # API
    url(r'^api/projects/(?P<project_id>[-\d]+)/etapes/$', prviews.api_get_actions, name='api_project_actions_list'),
    url(r'^api/add_etape_project/(?P<project_id>[-\d]+)$', prviews.api_add_etape_project, name='api_add_etape_project'),

    # API Django_rest DJANGO_REST
    url(r'^api/projects/$', prviews.ProjectList.as_view()),
    url(r'^api/project/(?P<pk>[-\d]+)$', prviews.ProjectDetail.as_view(), name='detail_project'),
    # API
    url(r'^api/members/(?P<project_id>[-\d]+)$',        prviews.MemberList.as_view()),
    url(r'^api/member/(?P<search_key>[a-zA-Z0-9]+)$',   prviews.MemberListFound.as_view()),
    url(r'^api/member/list/(?P<project_id>[-\d]+)$',    prviews.MemberProjectList.as_view()),
    # api add memebers
    url(r'^api/add_members/' , prviews.add_members ),
    url(r'^api/delete_member/(?P<project_id>[-\d]+)/(?P<member_id>[-\d]+)', prviews.delete_member_project, name='delete_event'),

    # users dispo
    url(r'^api/puser/(?P<user_id>[-\d]+)$', prviews.getUserProfile.as_view()),
    url(r'^api/users_dispo/(?P<project_id>[-\d]+)$', prviews.UserDispoList.as_view()),

    url(r'^api/tickets/$', tkviews.ticket_list, name='api_ticket_list'),
    url(r'^api/tickets/(?P<project_id>[-\d]+)$', tkviews.TicketsProjectList.as_view(), name='api_ticket_project_list'),
    url(r'^api/mestickets/(?P<user_id>[-\d]+)$', tkviews.MesTicketsProjectList.as_view(), name='api_mes_ticket_project_list'),
    url(r'^api/ticket/(?P<pk>[-\d]+)$', tkviews.ticket_detail, name='api_ticket_detail'),
    url(r'^api/ticket/(?P<search_key>[a-zA-Z0-9]+)$', tkviews.TicketListFound.as_view()),
    url(r'^api/update_ticket/(?P<task_id>[-\d]+)$', tkviews.update_ticket, name='update_ticket' ),
    url(r'^api/move_ticket/$', tkviews.move_ticket, name='move_ticket' ),
    # api exemple staff
    url(r'^api/get_staff/$', prviews.api_staff, name='api_staff' ),

    #
    # Upload
    url(r'^api/upload_doc/$', prviews.document_upload, name='doc_upload_ajax'),

    # callendar timeline
    url(r'^projects/timeline/$', prviews.ProjecTimeline.as_view() , name='project_timeline_calendar'),
    url(r'^api/projectevents/(?P<project_id>[-\d]+)$', prviews.ProjectEventsProject.as_view(), name='api_project_events'),
    url(r'^api/mesevents/$', prviews.MesEventsProject.as_view(), name='api_mes_events'),
    url(r'^api/mesresources/$', prviews.MesResourcesProject.as_view(), name='api_mes_resources'),
    # api contacte
    url(r'^api/add_ticket_contacte/$', tkviews.create_ticket_contacte , name='api_create_ticket_contacte'),

    #-----------------
    # APIVIEW Ticket
    #-----------------
    # Get event
    url(r'^api/ticket/(?P<pk>\d+)/$', tkviews.TicketDetail.as_view(), name='create_events_ticket'),
    # list all events
    url(r'^api/ticket/(?P<pk>\d+)/show/$', tkviews.TicketDetail.as_view(), name='list_events_ticket'),
    # url(r'^update$/(?P<pk>\d+)', #update event),
    url(r'^api/ticket/create/$', tkviews.TicketDetail.as_view(), name='create_events_ticket'),
    # delete event
    url(r'^api/ticket/(?P<pk>\d+)/delete/$', tkviews.MesTicketsProjectList.as_view(), name='delete_event_ticket'),
    # Api Service & Societe
    url(r'^api/get_services/(?P<societe_id>[-\d]+)$', prviews.ServicesSociete.as_view(), name='api_services_societe_list'),
    url(r'^api/get_societes/$', prviews.SocieteList.as_view(), name='api_societe_list'),
    # Api tickets stat
    url(r'^api/get_mesticket_stat/$', prviews.mes_ticket_stat, name='api_mestickets_list'),
    url(r'^api/get_project_ticket_stat/(?P<project_id>[\d]+)/$', prviews.api_ticket_project_stat, name='api_ticket_project_stat'),
    url(r'^api/get_project_ticket_stat3D/(?P<project_id>[\d]+)/$', prviews.api_ticket_project_stat3D, name='api_ticket_project_stat3D'),

    # Gantt
    url(r'^gantt/(?P<project_id>[-\d]+)$', prviews.showGantt.as_view(), name='project_chart_gantt'),
    url(r'^print/societe/$', businessviews.tree_societes,  name='tree_list_societes'),
    url(r'^print/chart/$', prviews.print_chart,  name='print_chart'),
    url(r'^print/chart3D/(?P<project_id>[-\d]+)/$', prviews.print_chart_3D,  name='print_chart_3d'),
    url(r'^print/piechart3D/(?P<project_id>[-\d]+)/$', prviews.print_piechart_3D,  name='print_piechart_3d'),
    # api toto
    url(r'^api/vtodo/(?P<user_id>\d+)/$', tkviews.TodoTodayList.as_view(), name='api_todo'),
    url(r'^api/vtodo/create/$', tkviews.TodoTodayList.as_view(), name='api_add_todo'),
    url(r'^api/vtodo/update/(?P<pk>[-\d]+)$',  tkviews.TodoTodayList.as_view(),  name='api_update_todo'),
    url(r'^api/vtodo/delete/(?P<pk>[-\d]+)$',  tkviews.TodoTodayList.as_view(),  name='api_del_todo'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ajout de sufixe au api url (.json, .api)
urlpatterns = format_suffix_patterns(urlpatterns)
