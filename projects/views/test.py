#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.contrib import messages
from django.core import serializers
from django.shortcuts import  redirect as  redirect_to, render, reverse, redirect

from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django import forms
from django.template import RequestContext
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required
from core.views import filtered_list_detail
from core.profile.models import Member
from django.views.generic.edit import FormMixin
from ofschedule.models import DjangoClient
# from ..models import *
from ..forms import ProjectForm, MemberProjectForm, TicketForm

from ..models import Project, Milestone, Ticket
from ..serializers import TicketSerializer, ProjectSerializer, MemberSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import Http404
from rest_framework.views import APIView


# @permission_required('projects.change_project', _get_project)
class testView(UpdateView):
    """Edit a new project.
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
        form.initial.update({
            'date_debut' : project.date_debut.strftime('%Y-%m-%d'),
        })
        #form.fields["date_debut"].initial = project.date_debut.strftime('%d/%m/%Y')
        context['form'] = form
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.author = self.request.user
        project.save()
        return redirect('project_detail', pk=project.pk,)
