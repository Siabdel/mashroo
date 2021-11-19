#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""
import os, sys, time
from django.http import JsonResponse
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.contrib import messages
from django.core import serializers
from django.shortcuts import  redirect as  redirect_to, render, reverse, redirect

from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, BaseListView
from django import forms

from django.template import RequestContext
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from core.views import filtered_list_detail
from django.views.generic.edit import FormMixin
from projects.models import DjangoClient
# from ..models import *
from  ..forms import ProjectForm, MemberProjectForm, TicketForm, DocumentForm, ProfileForm

from ..models import Project, Milestone, Ticket, Member
from ..serializers import TicketSerializer, ProjectSerializer, MemberSerializer, TicketsProjectSerializer
from .. import serializers  as pro_serialize
from core.taxonomy.models import Category
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import Http404
from rest_framework.views import APIView

from django import template
from django.contrib.contenttypes.models import ContentType
from .. import models as pro_models
from mashroo import settings

from ..utils import create_thumbnail, save_thumbnail
from core.profile.models import UProfile, Service, Societe
from django.contrib.auth.models import User
from notify.signals import notify
from datetime import timedelta


def _get_project(request, *args, **kwargs):
    code = kwargs.get('code', None)
    return get_object_or_404(Project, code=code)

# @permission_required('projects.view_project')
@method_decorator(login_required, 'dispatch')
class AccueilView(ListView):
    """
    Home page Project
    """
    template_name = "projects/index.html"
    model = Project

    def get_context_data(self,  **kwargs):
        context = super(AccueilView, self).get_context_data(**kwargs)
        # context['filter_fields'] = self.model.objects.all()
        context['user'] = self.request.user

        if self.request.user.has_perm("projects.change_project"):
            messages.success(self.request, _("j'ai la permission = projects.change_project"))

        return context

# @permission_required('projects.view_project')
@method_decorator(login_required, 'dispatch')
class ProjectHomeView(ListView):
    """
    Home page Project
    """
    template_name = "project_home.html"
    model = Project
    paginate = 25
    context_object_name = 'filtered_list'
    fields = ['code', 'title', 'author', 'manager', 'created', 'status']
    object_list = None

    def get_queryset(self, **kwargs):
        context = super(ProjectHomeView, self).get_context_data(**kwargs)
        ce_mois_ci = datetime.datetime.now().month
        cette_semaine = datetime.datetime.isocalendar(datetime.datetime.now())[1]
        cette_annee = datetime.datetime.isocalendar(datetime.datetime.now())[0]
        # mes projets et les projects ou je suis member
        if self.request.user.is_superuser :
            self.object_list = self.model.objects.filter(created__year=cette_annee).order_by('-created')
            return self.object_list


        mes_project = context['object_list'] = self.model.objects.filter(
            author=self.request.user,
            created__year=cette_annee
            ).order_by('-created')
        # member Membership projects
        mes_membership = pro_models.Membership.objects.filter( member__user = self.request.user).all()
        list_mes_projets_member = [ elem.project_id for elem in mes_membership ]

        mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member)
        #created__year=cette_annee )
        # messages.success(self.request, "filtre = %s "% self.object_list)
        # je selectionne mes projet et ceux de mes membre
        self.object_list = mes_project |  mes_projets_member
        # messages.success(self.request, "fmes_project et  mes_projets_member= %s "% self.object_list)

        return self.object_list


# @permission_required('projects.view_project')
@method_decorator(login_required, 'dispatch')
class ProjectHomeViewFiltre(ListView):
    """
    Home page Project
    """
    template_name = "project_home.html"
    model = Project
    paginate = 25
    context_object_name = 'filtered_list'
    fields = ['code', 'title', 'author', 'manager', 'created', 'status']
    object_list = None

    def get(self, request, filtre, **kwargs):
        context = self.get_context_data(**kwargs)
        ce_mois_ci = datetime.datetime.now().month
        cette_semaine = datetime.datetime.isocalendar(datetime.datetime.now())[1]
        cette_annee = datetime.datetime.isocalendar(datetime.datetime.now())[0]

        if filtre == 'closed':
            context['object_list'] = self.model.objects.filter(author=self.request.user, created__year=cette_annee, status='CLOSED').order_by('-created')
            # messages.success(self.request, "filtre = %s "% self.object_list)
            return render(request, self.template_name, context)

        options = {
            'status': 'OPEN',
            'created' :{
                'created_semaine':False,
                'created_mois':False,
                'created_annee':False,
            },

            'due_date' :{
                'due_semaine':False,
                'due_mois':False,
                'due_annee':False,
            },
        }
        ## topper le bon filtre
        if filtre in options['created'].keys():
            options['created'][filtre] = True
            # 1 liste de nouveau projet (semaine, mois, an)
            context['object_list'] = self.list_projets_nouveau(**options['created'] )

        elif filtre in options['due_date'].keys():
            options['due_date'][filtre] = True
            # 2 liste de nouveau projet (semaine, mois, an)
            context['object_list'] = self.list_projets_encours(**options['due_date'])

        # messages.success(self.request, "filtre = %s "% self.object_list)
        return render(request, self.template_name, context)


    def list_projets_nouveau(self,  **options ):
        mes_project = mes_projets_member = None
        ce_mois_ci = datetime.datetime.now().month
        cette_semaine = datetime.datetime.isocalendar(datetime.datetime.now())[1]
        cette_annee = datetime.datetime.isocalendar(datetime.datetime.now())[0]


        # 1- projets de cette semaine
        if options['created_semaine'] :
            # messages.success(self.request, r"filtre options={} annee={}".format(options, ce_mois_ci))
            mes_project = self.model.objects.filter(author=self.request.user, created__week=cette_semaine).order_by('-created')
        # projets de Ce mois ci
        elif options['created_mois']  :
            mes_project = self.model.objects.filter(author=self.request.user, created__month=ce_mois_ci).order_by('-created')
        elif options['created_annee'] :
            mes_project = self.model.objects.filter(author=self.request.user, created__year=cette_annee).order_by('-created')
        else :
            mes_project = self.model.objects.filter(author=self.request.user).order_by('-created')

        # 3- je selectionne mes projet et ceux de mes membre
        mes_membership = pro_models.Membership.objects.filter( member__user = self.request.user).all()
        list_mes_projets_member = [ elem.project_id for elem in mes_membership ]
        if options['created_semaine'] :
            mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member, created__week=cette_semaine )
        elif options['created_mois']  :
            mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member, created__month=ce_mois_ci )
        elif options['created_annee']  :
            mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member, created__year=cette_annee )

        # je selectionne mes projet et ceux de mes membre
        self.object_list = mes_project |  mes_projets_member
        # participan_projets  =  self.model.objects.filter(author__in=)
        return self.object_list

    def list_projets_encours(self,  **options ):
        mes_project = mes_projets_member = None
        ce_mois_ci = datetime.datetime.now().month
        cette_semaine = datetime.datetime.isocalendar(datetime.datetime.now())[1]
        cette_annee = datetime.datetime.isocalendar(datetime.datetime.now())[0]

        # 1- projets de cette semaine
        if options['due_semaine'] :
            mes_project = self.model.objects.filter(author=self.request.user, due_date__week=cette_semaine).order_by('-created')
        # projets de Ce mois ci
        elif options['due_mois']  :
            # messages.success(self.request, r"filtre options={} annee={} ".format(options, ce_mois_ci))
            mes_project = self.model.objects.filter(author=self.request.user, due_date__month=ce_mois_ci).order_by('-created')
        elif options['due_annee'] :
            mes_project = self.model.objects.filter(author=self.request.user, due_date__year=cette_annee).order_by('-created')
        else :
            mes_project = self.model.objects.filter(author=self.request.user).order_by('-created')

        # 3- je selectionne mes projet et ceux de mes membre
        mes_membership = pro_models.Membership.objects.filter( member__user = self.request.user).all()
        list_mes_projets_member = [ elem.project_id for elem in mes_membership ]
        if options['due_semaine'] :
            mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member, due_date__week=cette_semaine )
        elif options['due_mois']  :
            mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member, due_date__month=ce_mois_ci )
        elif options['due_annee']  :
            mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member, due_date__year=cette_annee )

        # je selectionne mes projet et ceux de mes membre
        if  mes_project  or  mes_projets_member:
            self.object_list = mes_project |  mes_projets_member
        # participan_projets  =  self.model.objects.filter(author__in=)
        return self.object_list


# @permission_required('projects.view_project')
@method_decorator(login_required, 'dispatch')
class ProjectListView(ListView):
    """
    Displays the list of all wiki pages.
    """
    template_name = "project_list.html"
    model = Project
    paginate = 25
    context_object_name = 'filtered_list'
    fields = ['code', 'title', 'author', 'manager', 'created', 'status']

    def get_context_data(self,  **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['filter_fields'] = self.model.objects.all()
        return context

    def get_queryset(self, **kwargs):
        """
        mes projets ou ceux dont je suis participants
        """
        if not self.request.user.is_superuser :
            mes_project = self.model.objects.filter(author=self.request.user).order_by('-created')
            mes_membership = pro_models.Membership.objects.filter( member__user = self.request.user).all()
            list_mes_projets_member = [ elem.project_id for elem in mes_membership ]
            mes_projets_member = self.model.objects.filter(pk__in = list_mes_projets_member )


            self.object_list = mes_project |  mes_projets_member
            # participan_projets  =  self.model.objects.filter(author__in=)

        else :
            self.object_list= self.model.objects.all().order_by('-created')

        return self.object_list


# @permission_required('projects.view_project', _get_project)

@method_decorator(login_required, 'dispatch')
class ProjectDetailView(FormMixin, DetailView ):
    """
    Displays the Details views
    """
    template_name = "project_detail.html"
    model = Project
    object = None
    form_class = MemberProjectForm


    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        form_members = MemberProjectForm(initial= { 'project' : self.object})
        participants  = [ member.pk for member in self.object.participants.all() ]
        # de la liste des user il faut enlever les participant deja inviter
        form_members.fields['user'].queryset = UProfile.objects.all().exclude(pk__in = participants)
        # form_members.fields['status'].widget = forms.HiddenInput()
        context['project_id'] = self.object.pk
        context['form_members'] = form_members
        context['current_user'] = self.request.user
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #form = MemberProjectForm(self.request.POST)

        form = self.get_form()
        if form.is_valid():
            form.save()
            if self.request.is_ajax():
                render_json_response(self, self.object)
            else :
                return render("/pro/project/%s" % self.object.pk, kwargs )
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)

    def render_json_response(self, queryset):
        """
        export json format
        """
        json_data = serializers.serialize('json', queryset)
        # Proceed to create your context object containing the columns and the data
        return HttpResponse(json_data, content_type='application/json')

import datetime

#@permission_required('projects.add_project')
@method_decorator(login_required, 'dispatch')
class ProjectCreateView(CreateView):
    """Adds a new project.
    """
    template_name = 'projects/project_edit.html'
    models = Project
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self, project_id):
        return reverse('project_detail', kwargs={'pk': project_id})

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView,
                        self).get_context_data(**kwargs)
        # coller une class css au elements du form fields[field].widget.attrs['class']
        form = self.get_form()
        #form.fields['slug'].widget.attrs['readonly']="readonly"
        form.initial.update({'manager' :  self.request.user })
        form.initial.update({'author' :  self.request.user })
        try :
            non_definie_cat = Category.objects.filter(title__icontains = "Non définie")
            form.initial.update({'category' : non_definie_cat.first().pk })
        except Exception as err:
            messages.success(self.request, _("pas de categorie non connue. %s " % err))

        ## init date debut
        aujourdhui = datetime.datetime.now()
        form.initial.update({'date_debut' : aujourdhui.strftime("%Y-%m-%dT%H:%M") })


        context['form'] = form
        return context

    def form_invalid(self, form):
        messages.add_message(self.request, messages.INFO, 'form is invalide !!!')
        return super(ProjectCreateView, self).form_invalid(form)


    def post(self, request):
        """
        surcharge form_valid
        """
        # maj Post date_debut
        # set to mutable
        """
        #request.POST._mutable = True
        request.POST.update(
            {'date_debut' :  datetime.datetime.strptime( request.POST.get('date_debut', False), "%Y-%m-%dT%H:%M") }
            )
        """
        form = ProjectForm(request.POST)
        # form.calendar = get_object_or_404(Calendar, slug=self.kwargs['calendar_slug'])
        # form.fields['date_debut'] =  datetime.datetime.strptime(request.POST.get('date_debut'), "%Y-%m-%dT%H:%M")
        # form.initial.update({'date_debut' :  "2019-12-17 13:31:00" })
        if form.is_valid():
            project = form.save(commit=False)
            form.instance.author    = self.request.user
            if form.data['clients'] :
                # messages.add_message(self.request, messages.INFO, 'add partenaire  %s ' % form.data['clients'] )
                partenaire_code = form.data['clients']
                partenaire = DjangoClient.objects.get(codeclie=partenaire_code)
            # save
            project.save()
            if form.data['clients'] :
                project.add_partenaire_client(partenaire_id=partenaire.codeclie, partenaire_name=partenaire.nomclie )
            #project.add_tags("Django framework")

            # Notifcations :
            ## Sending notifications to a single user
            notify.send(self.request.user, recipient=self.request.user, actor=self.request.user,
                verb='Votre projet code {} est creer .'.format(project.code), nf_type='project_home')

            # notify for a group user Sending notifications to multiple users MemberSerializer

            # notify for a group user Sending notifications to multiple users followers
            profile_user = pro_models.UProfile.objects.get(user=self.request.user)
            if len(profile_user.following.all()) > 0   :
                followers = list(profile_user.following )
                notify.send(self.request.user, recipient_list=followers, actor=self.request.user,
                            verb="Votre projet code {} est creer ".format(project.code), target=document, nf_type='followed_by_one_user')

        else :
            # messages.add_message(self.request, messages.INFO, 'form is invalide %s ' % form.data)
            return render(request, self.template_name, locals())

        return HttpResponseRedirect(self.get_success_url(project.id))

# @permission_required('projects.change_project', _get_project)
@method_decorator(login_required, 'dispatch')
class ProjectEditView(UpdateView):
    """
    Edit a new project.
    """
    template_name = 'projects/project_edit.html'
    model = Project
    form_class = ProjectForm
    pk_url_kwarg = 'pk'
    context_object_name = 'project'


    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        project = self.get_object()
        form = self.get_form()
        # adaptez le format de la date rendu au  FORMAT_DATE = "%Y-%m-%dT%H:%M"
        DATE_FORMAT = "%Y-%m-%dT%H:%M"
        form.initial.update ( {'date_debut': project.date_debut.strftime(DATE_FORMAT)})
        form.initial.update ( {'due_date': project.due_date.strftime(DATE_FORMAT)})

        #form.fields["date_debut"].initial = project.date_debut.strftime('%d/%m/%Y')
        # form.fields['date_fin'].widget = forms.HiddenInput()
        context['project_id'] = self.object.pk

        context['form'] = form
        context['model_id'] =  self.get_object().pk
        context['model_name'] = 'Project'
        # form upload
        context['form_file'] = DocumentForm()
        return context


    def form_valid(self, form):
        """
        valid
        """
        form.instance.auteur = self.request.user

        # Partenaire Client && Fournissuer
        project = form.instance
        if form.data['clients'] :
            ## voir si exist deja
            queryset  = form.instance.get_partenaires_project()
            client_id = form.data['clients']
            if not queryset.filter(tiers_id = client_id).exists():
                messages.add_message(self.request, messages.INFO, 'add partenaire  %s ' % form.data['clients'] )
                partenaire_code = form.data['clients']
                partenaire = DjangoClient.objects.get(codeclie=partenaire_code)
                project.add_partenaire_client(partenaire_id=partenaire.codeclie, partenaire_name=partenaire.nomclie )

        # Notifcations :
        message = "Votre projet code {} est modifier .".format(project.code)
        ## Sending notifications to a single user
        notify.send(self.request.user,
                    recipient=self.request.user,
                    actor=self.request.user,
                    verb=message, nf_type='project_home')


        # notify for a group user Sending notifications to multiple users MemberSerializer
        members = form.instance.participants.all()
        participants = [member.user for member in members]

        # notify for a group user Sending notifications to multiple users followers
        document = None
        if len(participants) > 0   :
            notify.send(self.request.user,
                        recipient_list=participants,
                        actor=self.request.user,
                        verb=message,
                        target=document, nf_type='followed_by_one_user')


        # ticket = get_object_or_404(Ticket, project=project, code=code)
        return super(ProjectEditView, self).form_valid(form)


# @permission_required('projects.delete_project', _get_project)
@method_decorator(login_required, 'dispatch')
class ProjectDeleteView(DeleteView):
    model = Project

    def get_success_url(self):
        return reverse('project_list')

# API
def render_json_response(queryset):
    """
    export json format
    """
    json_data = serializers.serialize('json', queryset)
    # Proceed to create your context object containing the columns and the data
    return HttpResponse(json_data, content_type='application/json')


def api_get_actions(request, project_id):
    # liste des actions
    queryset_actions = Ticket.objects.filter(project=project_id).order_by("-created")
    #
    return render_json_response(queryset_actions)

def api_add_etape_project(request, project_id):
    """ """
    sujet = request.POST.get('title')
    form = TicketForm(request.POST)


    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO,
                             'api_add_etape_project.  %s ' % request.POST)
    else :
        errors = [(field.errors, field.label) for field in form]
        messages.add_message(request, messages.INFO,
                             'api_add_etape_project.  %s ' % errors )

    return HttpResponse({ 'message': sujet}, content_type='application/json')

import json


@method_decorator(login_required, 'dispatch')
class ProjectList(APIView):
    """
    List all projects, or create a new project.
    """
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, 'dispatch')
class MemberList(APIView):
    """
    List all members
    """
    def get(self, request, project_id, format=None):
        members = Project.objects.get(pk=project_id).list_members()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, 'dispatch')
class MemberListFound(APIView):
    """
    List  members found
    """

    def get(self, request, search_key, format=None):
        search = self.kwargs
        list_total  = [ f.name for f in  UProfile._meta.get_fields()]

        members = UProfile.objects.filter(user__username__icontains=search_key).order_by("user__username")

        """
        members = members.values_list('id', 'user__username', 'user__email',
                                   'timezone', 'date_naissance', 'photo',
                                   'fonction', 'service', 'language', 'role')
        """
        #
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


class UserDispoList(APIView):
    """
    List all users dispos
    """
    def get(self, request, project_id, format=None):
        search = self.kwargs
        project = Project.objects.get(pk=project_id)
        members = project.list_members()
        users_dispo =  UProfile.objects.all().exclude(pk__in=[elem.pk for elem  in members])
        serializer = MemberSerializer(users_dispo, many=True)
        return Response(serializer.data)

class getUserProfile(APIView):
    """
    List all users dispos
    """
    def get(self, request, user_id, format=None):
        user = get_object_or_404(pro_models.UProfile, user__id = user_id)
        serializer = MemberSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = get_object_or_404(pro_models.UProfile, user__id = user_id)
        serializer = MemberSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(pro_models.UProfile, user__id = user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MemberProjectList(APIView):
    """
    List all users dispos
    """
    def get(self, request, project_id, format=None):
        search = self.kwargs
        if project_id :

            try :
                project = Project.objects.get(pk=project_id)
                members = project.list_members()
                serializer = MemberSerializer(members, many=True)
                return Response(serializer.data)

            except Exception as err :
                return Response("project {} not found !".format(project_id), status=status.HTTP_400_BAD_REQUEST)


##
class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE' ])
def project_detail(request, pk, format=None):
    """
    api project_list s'occupe des demande GET, UPDATE et DELETE
    """

    try :
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' :
        project_serialise = ProjectSerializer(project)
        return Response(project_serialise.data)

    elif request.method == 'PUT':
        project_serialise = ProjectSerializer (project, data=request.data)
        if project_serialise.is_valid() :
            project_serialise.save()
            return Response(project_serialise.data)
        else :
            return Response(project_serialise.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST','DELETE'])
def delete_member_project(request, project_id, member_id, format=None):
    """
    api  DELETE member of project
    """

    try :
        member = pro_models.Membership.objects.get(project_id=project_id, member_id=member_id)
    except pro_models.Membership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Add members  project
### @api_view(['GET', 'PUT', 'DELETE' ])
def add_members(request, format=None):
    """
    api pour jouter de membre au projet
    """
    if request.method == 'POST':
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            data = json_data
            project_id = data["project"]
            members = data["members"]
            project = Project.objects.get(pk=project_id)
            # add members
            for member_id in members:
                mm = UProfile.objects.get(pk=member_id)
                project.add_member(mm)
                # messages.add_message(request, messages.INFO, "api add membre au projet {}".format(members))

        except Exception as err:
            # messages.add_message(request, messages.INFO, "api err {} members={}".format(err.message, json_data))
            return JsonResponse({"message": err.message})


        return JsonResponse({"message": request.POST})

    else :
        return JsonResponse({"rien ": request.method})


register = template.Library()
@register.inclusion_tag('project/element/_partenaire.html')
def get_partenaire(related_object):
    related_object_type = ContentType.objects.get_for_model(related_object)
    parts = Partenaire.objects.filter(
        content_type__pk=related_object_type.id,
        object_id=related_object.id,
    ).first()
    return {
        'partenaire': parts,
    }


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
            'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

@method_decorator(login_required, 'dispatch')
class MemberCreate(AjaxableResponseMixin, CreateView):
    model = Member
    fields = ['id', 'name', ]

#------------
#-- TOTO
#-----------
@login_required
def todo_today(request):
    user = request.user
    return render(request, template_name="todo/index.html", context=locals())

#-----------
#-- PROFILE
#-----------
def notification_list(request):
    return render(request, template_name="boite_reception.html")
#------------
#-- PROFILE
#-----------
@method_decorator(login_required, 'dispatch')
class MyProfileDetailView(DetailView):
    template_name = "projects/profile_user.html"
    model = UProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        societes =  Societe.objects.filter(pk=2).order_by('name')
        context['societes'] = societes
        return context


    def get(self, request, user_id,  *args, **kwargs):
        #self.object = pro_models.UProfile.objects.get(user__id=self.request.user.pk)
        self.object = get_object_or_404(pro_models.UProfile, user__pk=user_id)

        context = {'object': self.object}
        # messages.add_message(self.request, messages.INFO, ' get_queryset user %s' %  self.object)
        return render(request, "projects/profile_user.html", context)


@method_decorator(login_required, 'dispatch')
class MyProfileEditView(UpdateView):
    template_name = "projects/profile_edit.html"
    model = UProfile
    form_class =  ProfileForm
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'



    def get_context_data(self,  **kwargs):
        context = super(MyProfileEditView, self).get_context_data(**kwargs)
        project = self.get_object()
        form = self.get_form()
        # form.fields["date_debut"].initial = project.date_debut.strftime('%d/%m/%Y')
        if not self.request.user.is_superuser :
            # form.fields['role'].widget = forms.HiddenInput()
            #form.fields['role'].widget.attr['readonly'] = 'readonly'
            pass

        context['object'] = project
        context['form'] = form
        return context


    def get(self, request, user_id, *args, **kwargs):
        self.object = get_object_or_404(pro_models.UProfile, user__pk=user_id)
        context = self.get_context_data(**kwargs)
        form = self.get_form()

        if settings.SOCIETE:
            societe_id =  settings.SOCIETE

            try :
                query_service = Service.objects.filter(societe_id=societe_id).values_list( 'id', 'name' ).order_by('name')
                services_choice  = [ (id, name[:20]) for ( id, name) in query_service.iterator() ]
                form.fields['service'].widget.choices = services_choice
                # form.initial.update({'service' :  services_choice } )
                form.initial.update({'societe' :  societe_id,
                                     'service' : self.object.service,
                                     'email' : self.object.user.email
                                     } )
                context['form'] = form

            except Exception as err :
                messages.add_message(self.request, messages.INFO, 'erreur = %s' %  err.message )
                pass

        # profil
        societes =  Societe.objects.filter(pk=2).order_by('name')
        context['societes'] = societes
        return render(request, "projects/profile_edit.html", context)

    def form_valid(self, form):
        if form.is_valid():
            profile = form.save(commit=False)
            # messages.add_message(self.request, messages.INFO, ' request = %s' %  form.cleaned_data )
            if form.cleaned_data['del_photo'] == 'True':
                profile.photo = None
            if form.cleaned_data['email'] :
                profile.user.email = form.cleaned_data['email']
                profile.user.save()

            profile.save()
            # document = pro_models.Document.objects.get(pk=100)
            return redirect(reverse('profile_user', kwargs={'user_id' : self.object.user.pk }) )

        return super(MyProfileEditView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('profile_user', kwargs={'user_id' : self.object.user.pk })


## Upload files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'csv', 'png', 'xsl', 'mp4'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
def document_upload(request):
    """
    """
    data = {'message': 'ok'}

    if request.method == 'POST':
        model_name  = request.POST.get("model_name")
        model_id    = request.POST.get("model_id")

        try :
            if model_name and model_name == 'Project':
                parent = Project.objects.get(pk=model_id)
            elif model_name and model_name == 'Ticket' :
                parent = Ticket.objects.get(pk=model_id)

        except Project.DoesNotExist  as err:
            data = {'message': 'ko'}
            messages.add_message(request, messages.INFO, 'DoesNotExist   %s' %  model_name)

            return JsonResponse(data)
        ## --

        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'doc active  %s' %  form.cleaned_data['active'])
            file = request.FILES['document']
            # positionner le flag active:
            if form.cleaned_data['active']  :
                dd = parent.documents.all()
                for doc in dd :
                    if doc.document.active :
                        dd = doc.document
                        dd.active = False
                        # messages.add_message(request, messages.INFO, "document active  = {} ".format(doc))

                        dd.save()


            # if user does not select file, browser also
            # submit an empty part without filename
            if file.name == '':
                data = {'message': 'No file select'}
                return JsonResponse(data)

            # save
            if file and allowed_file(file.name):
                instance = form.save(commit=False)

                # sauvegarde Document en base
                instance.save()

                instance.file_basename = os.path.basename(instance.document.name).lower()
                instance.file_size = instance.document.size
                #instance.file_type = instance.document.name.split('.')[1] # recuperer le type du fichier
                instance.file_type = instance.document.name.rsplit('.', 1)[1].lower()
                instance.initial_name = instance.file_basename
                #---------------------------
                # rename le fichier uploaded
                """ dd : (document', 'file_basename', 'file_size', 'file_type', 'from_db', 'full_clean')
                """
                # messages.add_message(request, messages.INFO, 'doctype %s' %  instance.full_clean)
                initial_path = instance.document.path

                django_type = instance.document
                aujourdhui = datetime.datetime.now()
                compteur_time = aujourdhui.strftime("%Y") +  "-" + str(time.time()).replace('.', '-')[4:]
                instance.document.name = "documents/piecejdoc_" +  compteur_time + "."  + instance.file_type
                # basename change
                instance.file_basename = os.path.basename(instance.document.name).lower()
                new_path = settings.MEDIA_ROOT + instance.document.name
                thumbnail_name =  settings.MEDIA_ROOT + "documents/thumbnail_" +  compteur_time + "."  + "jpeg"

                # sauvegarde Document en base
                instance.save()

                # Move the file on the filesystem
                #messages.add_message(request, messages.INFO, "form post  = {} ".format(form.cleaned_data))
                # messages.add_message(request, messages.INFO, "initial_path  = {} new_path= {}".format(initial_path, new_path))
                os.rename(initial_path, new_path)


                # create a thumbnail Image
                extension = instance.document.name.rsplit('.', 1)[1].lower()
                basename  = os.path.split(instance.document.name)[-1]
                directory = os.path.split(instance.document.name)[0]
                # create_thumbnail
                if extension in ('jpeg' , 'jpg', 'png', 'gif'):
                    # messages.add_message(request, messages.INFO, ' filename %s' %  new_path)
                    if create_thumbnail(new_path, thumbnail_name,  extension) == True :
                        # save_thumbnail(document_file, document_fullname)
                        # save_thumbnail(instance.document.file, new_path)
                        instance.thumbnail_file = os.path.basename(thumbnail_name).lower()
                        pass



                # add document
                parent.add_document(instance)

        else :
            messages.add_message(request, messages.INFO, 'form invalide !! %s' % form.errors)

    else:
        form = DocumentForm()
    #
    return JsonResponse(data)


@method_decorator(login_required, 'dispatch')
class ProjecTimeline(ListView):
     """
     timeline calendar
     var url_resources = `{% url 'api_mes_resources'  %}`;
 	 var url_events = `{% url 'api_mes_events'  %}`;
     """
     model = Project
     template_name = "elements/timeline_calendar.html"

     def get_context_data(self,  **kwargs):
        context = super(ProjecTimeline, self).get_context_data(**kwargs)
        aujourdhui = datetime.datetime.now().strftime("%Y-%m-%d")
        # "2020-01-09"
        context['default_date'] = aujourdhui

        resources = [
            { 'id': "a", 'title': "Room A" , 'eventColor': "black"},
            { 'id': "b", 'title': "Room B", 'eventColor': "green" },
            { 'id': "c", 'title': "Room C", 'eventColor': "orange" },
            { 'id': "d", 'title': "Room D", 'eventColor': "red" }
        ]

        events = [
            { 'id': "1", 'resourceId': "a", 'start': "2020-02-24", 'end': "2020--03-11", 'title': "event 1" },
            { 'id': "2", 'resourceId': "a", 'start': "2020-02-24", 'end': "2020--03-11", 'title': "event 2" },
            { 'id': "3", 'resourceId': "b", 'start': "2020-02-24", 'end': "2020--03-11", 'title': "event 3" },
            { 'id': "4", 'resourceId': "c", 'start': "2020-02-24", 'end': "2020-03-01", 'title': "event 4" },
            { 'id': "5", 'resourceId': "d", 'start': "2020-02-24", 'end': "2020-03-11", 'title': "event 5" }
        ]

        context['events'] = events
        context['resources'] = resources
        resources = json.dumps(resources, ensure_ascii=False)
        return context


@method_decorator(login_required, 'dispatch')
class MesEventsProject(APIView):
    """
    List all events
    from django.db.models import F, Value
    tt.update(end_date = F('created'))
    """
    def get(self, request,  format=None):

        if request.user.username == 'admin':
            tickets = Ticket.objects.filter(assignee=request.user).order_by("-id")
        else :
            tickets = Ticket.objects.filter(assignee=request.user).order_by("-id")

        serializer = pro_serialize.TicketTimelineEventsSerializer(tickets, many=True)
        # serializer =  json.dumps(events, ensure_ascii=False)
        return Response(serializer.data)


from django_pandas.io import read_frame
import pandas as pd

def api_staff(request):
    """
    List all memeber of staff
    Out[16]: '{ }'
    """
    employees = { "data": [
        {
          "firstName":"Abdel",
          "lastName":"Sadquaoui",
          "photo": "images/photo1.jpeg",
          "email" : "abdel2@gmail.com",
          "telephone": "0675441123",
          "service" : "Informatique",
        },

        {
          "firstName":"Christine",
          "lastName":"Delphin",
          "photo": "images/photo22.jpeg",
          "email" : "christine.delphin@strandcosmeticseurope.com",
          "telephone": "0478129918",
          "service" : "Informatique",
        },
      ]
    }
    # events = employees.to_json()
    #
    # serializer =  json.dumps(employees, ensure_ascii=False)
    # voir en claire
    # serializer =  json.loads(employees)
    # json_data = serializers.serialize('json', employees)
    return JsonResponse(employees)



def mes_ticket_stat(request):
    """
    List all events for user
    status
    encours   1
    nouveau   6
    data.to_json()
    Out[16]: '{"id":{"encours":1,"nouveau":6}}'
    """
    tickets =  Ticket.objects.filter(assignee_id=2).values('status', 'id').order_by("-id")
    df = read_frame(tickets, fieldnames=[ 'id',  'status'])
    data = df.groupby('status').count()
    # events = data.to_json()
    events = data.to_json()
    #
    # serializer =  json.dumps(events, ensure_ascii=False)
    # envoir en claire
    serializer =  json.loads(events)

    return JsonResponse(serializer)

#------------------------
#--ticket_project_stat
#------------------------
def api_ticket_project_stat(request, project_id):
    """
    List all events for project
    status
    encours   1
    nouveau   6
    data.to_json()
    Out[16]: '{"nouveau": 2, "enattente": 0, "cloturee": 2, "encours": 1, "resolue": 4, "message": "un report sur les tickets project "}'
    """
    tickets =  Ticket.objects.filter(project__id=project_id).values('status', 'id').order_by("-id")
    df = read_frame(tickets, fieldnames=[ 'id',  'status'])
    data = df.groupby('status').count()
    total_tickets = df.groupby('status').sum()
    # events = data.to_json()
    events = data.to_json()
    #
    # serializer =  json.dumps(events, ensure_ascii=False)
    # envoir en claire
    serializer =  json.loads(events)
    dict_stat = data.to_dict()

    dict_complet = {'nouveau':0, 'encours':0, 'resolue':0, 'cloturee':0, 'enattente':0}

    for key in ['nouveau', 'encours', 'resolue', 'cloturee', 'enattente'] :
        try :
            dict_stat['id'][key]
            dict_complet[key] = dict_stat['id'][key]
        except :
            dict_complet[key] = 0

    # récuperation du titre
    try:
         pp = Project.objects.get(id=project_id)
         title = pp.title
    except Exception as err :
        title = ""

    dict_complet['project_name'] =  title

    dict_complet['total_tickets'] = df['status'].count()


    return JsonResponse(dict_complet)


#------------------------
#--ticket_project_stat 3D
#------------------------

ORANGE  = "#FF7F00"
YELLOW  = "#FFFF00"
RED     = "#FF1111"
YELLOW_CITRON = "#F7FF3C"
GREEN       = "#008000"
GREEN_APPLE = "#8db600"
LIGHTBLUE   = "#ADD8E6"
GREY    = "#DCDCDC"

def api_ticket_project_stat3D(request, project_id):
    """
    List all events for project
    {
    "status": "nouveau",
    "taches": 4025,
    "color": "#FF0F00"
    },

    Out[16]: {'nouveau':0, 'encours':0, 'resolue':0, 'cloturee':0, 'enattente':0}
    """
    tickets =  Ticket.objects.filter(project__id=project_id).values('status', 'id').order_by("-id")
    df = read_frame(tickets, fieldnames=[ 'id',  'status'])
    data = df.groupby('status').count()
    # events = data.to_json()
    events = data.to_json()
    #
    # serializer =  json.dumps(events, ensure_ascii=False)
    # envoir en claire
    serializer =  json.loads(events)
    dict_stat = data.to_dict()
    data_response = []


    dict_complet = [{
        "status": "nouveau",
        "taches": 0,
        "color": YELLOW_CITRON
        },{
            "status": "encours",
            "taches": 0,
            "color": ORANGE
            },
        {   "status": "resolue",
            "taches": 0,
            "color": GREEN
            },
        {
            "status": "cloturee",
            "taches": 0,
            "color": GREEN_APPLE
            },

        {   "status": "annulee",
            "taches": 0,
            "color": GREY
            },
        {
            "status": "enattente",
            "taches": 0,
            "color": LIGHTBLUE
            }
        ]

    for key in ['nouveau', 'encours', 'resolue', 'cloturee', 'enattente'] :
        try :
            dict_stat['id'][key]
            for elem in dict_complet :
                if key == elem['status'] :
                    elem['taches'] = dict_stat['id'][key]
                    data_response.append(elem)
        except :
           elem['taches']  = 0
           data_response.append(elem)


    return JsonResponse({'data': data_response})

@method_decorator(login_required, 'dispatch')
class ProjectEventsProject(APIView):
    """
    List all events of project
    from django.db.models import F, Value
    tt.update(end_date = F('created'))
    """

    def get(self, request, project_id,  format=None):
        ##
        ligne =  {'name': "Planned", 'start': "2020-01-11T16:02:04", 'end': "2020--03-11", 'color': "#f0f0f0" }
        ligne_data = { 'id': 1, 'name':  "Feature 999", 'series': [],  }
        data = []
        #
        """
        Les taches ENCOURS avec une due_date et start_date
        """
        try :
            aujourdhui = datetime.datetime.now()
            tickets = Ticket.objects.filter(project_id=project_id,
                                            #due_date__gte=aujourdhui,
                                            status__in=('NOUVEAU', 'ENCOURS', 'ENATTENTE', 'RESOLUE', 'CLOTUREE')).order_by("-id")
        except Exception as err :
            return Response({'message': err.message})


        if tickets.count() > 1 :
            # project

            ligne_data = { 'project_id': 1, 'name':  "Project 999", 'due_date':'', 'series': [],  }
            ligne_data.update({ 'project_id' : project_id})
            ligne_data.update({ 'due_date' : tickets.first().project.due_date.strftime("%Y-%m-%d")} )
            ligne_data.update({ 'name' : tickets.first().project.code})
            # ligne project delai_due_date
            ligne =  {
                    'id': 999,
                    'project_id': tickets.first().id,
                    'name': tickets.first().project.title[:25],
                      'start': tickets.first().project.date_debut.strftime("%Y-%m-%d"),
                      'end': tickets.first().project.due_date.strftime("%Y-%m-%d"), 'color': "#f0f0f0" }

            ligne_data['series'].append( ligne )

            serializer = pro_serialize.TicketTimelineEventsSerializer(tickets, many=True)

            heure = 0
            for elem in tickets :
                # heure += 8
                if elem.created and elem.due_date :
                    ligne =  {'name': "",
                              'user': "",
                              'start': "",
                              'end': "", 'color': "#f0f0f0" }

                    ligne.update({ 'id' : elem.id})
                    ligne.update({ 'status' : elem.status})
                    if elem.assignee :
                        ligne.update({ 'user' : elem.assignee.username})
                        ligne.update({ 'name' : elem.assignee.first_name[0] +
                                                elem.assignee.last_name[0] +
                                                "-->" + elem.title[:30]})

                    else:
                        ligne.update({ 'user' : ''})

                    if elem.start :
                        ligne.update({ 'start':  (elem.start + timedelta(days=0, hours=-heure)).strftime("%Y-%m-%d")})
                    else :
                        ligne.update({ 'start':  (elem.created + timedelta(days=0, hours=-heure)).strftime("%Y-%m-%d")})

                    if elem.end :
                        ligne.update({ 'end':  (elem.end + timedelta(days=0, hours=heure)).strftime("%Y-%m-%d") })
                    else :
                        ligne.update({ 'end':  (elem.due_date + timedelta(days=0, hours=heure)).strftime("%Y-%m-%d") })

                    # ligne.update({ 'color': elem.eventColor})
                    ligne.update({ 'color': elem.eventColor})
                    ##
                    ligne_data['series'].append( ligne )

            data.append(ligne_data)

        serializer =  json.dumps(ligne_data, ensure_ascii=False)
        # return Response(serializer.data)
        return Response(data)



@method_decorator(login_required, 'dispatch')
class MesResourcesProject(APIView):
    """
    List all resources
    """
    def get(self, request,  format=None):

        tickets = Ticket.objects.filter(author=request.user).values('project').distinct()
        project_list_pk = [elem['project'] for elem in tickets ]

        projects = Project.objects.filter( pk__in=project_list_pk).order_by("-id")

        serializer = pro_serialize.TicketTimelineResourcesSerializer(projects, many=True)
        # serializer =  json.dumps(events, ensure_ascii=False)
        return Response(serializer.data)


@method_decorator(login_required, 'dispatch')
class showGantt(ListView):
     """
     timeline calendar
     """
     model = Project
     template_name = "project_gantt.html"

     def get(self,request, project_id, *args, **kwargs):
        """
        """
        #resources = json.dumps(resources, ensure_ascii=False)
        return render(request, self.template_name, context={'project_id' : project_id })



@method_decorator(login_required, 'dispatch')
class ServicesSociete(APIView):
    """
    List all services
    """
    def get(self, request,  societe_id, format=None):

        services = Service.objects.filter(societe=societe_id).order_by("-name")
        societe_list_service = [(elem.id, elem.name) for elem in services ]
        serializer = pro_serialize.ServiceSerializer(services, many=True)
        # serializer =  json.dumps(events, ensure_ascii=False)
        return Response(serializer.data)



@method_decorator(login_required, 'dispatch')
class SocieteList(APIView):
    """
    List all societes
    """
    def get(self, request,   format=None):

        societes = Societe.objects.all().order_by("-name")
        serializer = pro_serialize.SocieteSerializer(societes, many=True)
        # serializer =  json.dumps(events, ensure_ascii=False)
        return Response(serializer.data)

# ------------------------
# CHART
# -----------------------
def print_chart(request):
    """
    """
    template = "businessce/project_chart.html"
    return render(request, template, context=locals())


def print_chart_3D(request, project_id):
    """
    """
    template = "projects/elements/chart/project_3D_chart.html"
    return render(request, template, context=locals())


def print_piechart_3D(request, project_id):
    """
    """
    template = "projects/elements/chart/project_3D_piechart.html"
    return render(request, template, context=locals())
