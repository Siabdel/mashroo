#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2019 Strand Cosmetics'
__version__ = '0.9'
import datetime
from django.utils import timezone
from django.shortcuts import render_to_response, get_object_or_404, render, render_to_response, HttpResponseRedirect, reverse
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from core.views import filtered_list_detail
from django import forms
from ..forms import TicketForm, DocumentForm
from ..models import Ticket, Project, Vtodo
from core.taxonomy.models import Category
# API rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import Http404
from rest_framework.views import APIView

from ..serializers import TicketSerializer, ProjectSerializer, MemberSerializer, TicketsProjectSerializer
from ..serializers import TodoTodaySerializer
from core.profile.models import UProfile
from django.contrib.auth.models import User
from notify.signals import notify
import json
from django.core.mail import send_mail
from ..utils import send_html_email

def _get_ticket(request, *args, **kwargs):
    code = kwargs.get('code', None)
    project_code = kwargs.get('project', None)
    return get_object_or_404(Ticket, code=code, project__code=project_code)

# @permission_required('projects.view_ticket')
@method_decorator(login_required, 'dispatch')
class TicketListView(ListView):
    """Displays the list of all tickets of a specified project.
    """
    template_name='ticket_list.html'
    model = Ticket

    # all_tickets = project.tickets.all()
    fields = ['code', 'title', 'parent', 'author', 'manager', 'created', 'closed', 'urgency', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['now'] = timezone.now()
        return context
    def get_queryset(self, **kwargs):
        self.object_list = self.model.objects.all().order_by("-created")
        return self.object_list

@method_decorator(login_required, 'dispatch')
class MyTicketsListView(ListView):
    template_name='ticket_list.html'
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(MyTicketsListView, self).get_context_data(**kwargs)
        # project # ID
        self.object = get_object_or_404(Project, pk=kwargs['pk'])
        context['current_user'] = self.request.user
        context['now'] = timezone.now()

        return context

    def get(self, request, *args, **kwargs):
        #self.object = pro_models.UProfile.objects.get(user__id=self.request.user.pk)
        self.object_list = self.model.objects.all()
        context = {'object_list': self.object_list}
        return render(request, self.template_name, context)

#@permission_required('projects.add_ticket')
@method_decorator(login_required, 'dispatch')
class TicketAddView(CreateView):
    """Add a neww
    """
    template_name = 'ticket_edit.html'
    model = Ticket
    form_class =  TicketForm
    context_object_name = 'project'
    object = None
    project = None

    def get(self, request, project_id, *args, **kwargs):
        self.project  = get_object_or_404(Project, id=project_id)
        context = self.get_context_data(**kwargs)

        context['project'] = self.project
        context['project_id'] = self.project.pk

        return render(request, self.template_name, context)

    def get_context_data(self,  **kwargs):
        context = super(TicketAddView,  self).get_context_data(**kwargs)
        form = self.get_form()

        # saisir les données connu
        form.initial.update( {
                            'project': self.project,
                             'author' :  self.request.user,
                             'sequence' : 10})

        # form.fields['project'].widget =  Project.objects.get(pk=project_id)
        form.fields['author'].widget = forms.HiddenInput()
        form.fields['project'].widget = forms.HiddenInput()
        form.fields['sequence'].widget = forms.HiddenInput()
        aujourdhui = datetime.datetime.now()
        form.initial.update({'schedule_date' : aujourdhui.strftime("%Y-%m-%dT%H:%M") })
        try :
            non_definie_cat = Category.objects.filter(title__icontains = "non définie")
            form.initial.update({'category' : non_definie_cat.first().pk })
        except Exception as err:
            messages.success(self.request, _("pas de categorie non connue. %s " % err.message))
            pass

        context['form'] =  form
        return context

    def form_valid(self, form):
        """
        valid
        if milestone is not None:
            milestone = get_object_or_404(Milestone, code=milestone, project=project)
            initial['milestone'] = milestone
        """

        # messages.success(self.request, _("Your ticket has been registered. %s " % self.request.POST))

        ticket = form.save(commit=False)
        ##
        kwargs = self.get_form_kwargs()
        ticket.author = self.request.user
        ticket.save()
        #------------------
        # send email == un signal est connecter sur post_save
        #------------------
        #------------------
        # Notification
        #---------------
        TICKET_URL =  "http://" + self.request.get_host() + reverse('ticket_detail', kwargs={'pk' : ticket.id})

        message1 = u'Project Sce Send email : Your ticket has been registered.'
        message2 = u'Une tache no : {} a été ajouté a votre espace de travail !. le lien ici {}'.format(ticket.id, TICKET_URL)
        message3 = u'Une tache a été ajouté a votre espace de travail' 

        if ticket.assignee :
            notify.send(self.request.user,
                        recipient = ticket.assignee,
                        actor = self.request.user,
                        verb = message3,
                        nf_type = 'project_home')
        # notify for a group user Sending notifications to multiple users MemberSerializer
        members = ticket.project.participants.all()
        participants = [member.user for member in members]

        # notify for a group user Sending notifications to multiple users followers
        document = None
        if len(participants) > 0   :
            notify.send(self.request.user,
                        recipient_list=participants,
                        actor=self.request.user,
                        verb=message3,
                        target=document,
                        nf_type='followed_by_one_user')

        #----------------
        # retour
        #----------------
        success_url = reverse('project_detail', kwargs={'pk' : ticket.project.id})
        return HttpResponseRedirect(success_url)

    def del_milestone(self, form):
        if not self.request.user.has_perm("projects.change_milestone"):
            del form.fields['milestone']

        if not self.request.user.has_perm("projects.change_assignee"):
            del form.fields['assignee']



#@permission_required('projects.change_ticket', _get_ticket)
@method_decorator(login_required, 'dispatch')
class TicketEditView(UpdateView):
    """
    Update a ticket
    """
    template_name = 'ticket_edit.html'
    model = Ticket
    form_class =  TicketForm

    def get_context_data(self, **kwargs):
        context = super(TicketEditView, self).get_context_data(**kwargs)
        ticket  = self.get_object()
        form = self.get_form()
        # adaptez le format de la date rendu au  FORMAT_DATE = "%Y-%m-%dT%H:%M"
        DATE_FORMAT = "%Y-%m-%dT%H:%M"
        form.initial.update ( {'due_date': ticket.due_date.strftime(DATE_FORMAT)})
        form.initial.update ( {'schedule_date': ticket.schedule_date.strftime(DATE_FORMAT)})


        context['current_user'] = self.request.user
        context['object'] = ticket
        context['form'] = form
        context['project_id'] = self.get_object().project.pk

        context['model_id'] =   self.get_object().pk
        context['model_name'] = 'Ticket'
        # !! creer un bug car models porte 2 champs title et description qui sont aussi dans models ticket
        context['form_file'] = DocumentForm()

        return context

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk' : self.object.project.id})
        #return reverse('ticket_detail', kwargs={'pk' : self.object.id})

    def form_valid(self, form):
        """
        valid
        if milestone is not None:
            milestone = get_object_or_404(Milestone, code=milestone, project=project)
            initial['milestone'] = milestone
        """
        form.instance.auteur = self.request.user

        ## Sending notifications to a single user
        # message = u"Une tache modifer sur le projet code : {}".format(form.instance.project.code)
        message = u"Une tache modifer dans votre espace de travail"
        ticket = form.instance
        if ticket.assignee :
            notify.send(self.request.user,
                        recipient = ticket.assignee,
                        actor=self.request.user,
                        verb=message, nf_type='project_home')


        # notify for a group user Sending notifications to multiple users MemberSerializer
        members = ticket.project.participants.all()
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
        return super(TicketEditView, self).form_valid(form)


#@permission_required('projects.delete_ticket', _get_ticket)
class TicketDeleteView(DeleteView):
    """Update a ticket
    """
    template_name = 'confirm_delete.html'
    model = Ticket


#@permission_required('projects.view_ticket', _get_ticket)
@method_decorator(login_required, 'dispatch')
class TicketDetailView(DetailView):
    """Show ticket details.
    """
    template_name='projects/ticket_detail.html'
    model = Ticket


def ticket_detail(request, project, code, **kwargs):
    """Show ticket details.
    """
    project = get_object_or_404(Project, code=project)
    ticket = get_object_or_404(Ticket, project=project, code=code)
    object_list = project.tickets.all()
    return list_detail.object_detail(
        request,
        object_id=ticket.pk,
        queryset=object_list,
        extra_context={'object_list': object_list},
        **kwargs
    )



class TicketDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    curl -X DELETE "http://127.0.0.1:8000/api/project/delete/1"
    """

    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ticket = self.get_object(pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ticket = self.get_object(pk)
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ticket = self.get_object(pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    def post(self, request, format=None):
        serializer = TicketSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE' ])
def ticket_detail(request, pk, format=None):
    """
    api project_list s'occupe des demande GET, UPDATE et DELETE
    """
    try :
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' :
        ticket_serialise = TicketSerializer(ticket)
        return Response(ticket_serialise.data)

    elif request.method == 'PUT':
        ticket_serialise = TicketSerializer (ticket, data=request.data)
        if ticket_serialise.is_valid() :
            ticket_serialise.save()
            return Response(ticket_serialise.data)
        else :
            return Response(ticket_serialise.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# api update task
### @api_view(['GET', 'PUT', 'DELETE' ])
def create_ticket_contacte(request,  format=None):
    """
    api pour creer des ticket contacte user dans le portail
    """
    if request.method == 'PUT':
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            data = json_data
            nom     = data["nom"]
            email   = data["email"]
            message = data["message"]
            # projet support retour des ticket bug par client
            project, created  = Project.objects.get_or_create(title="recolte message client")
            task = Ticket.objects.create(project=project,
                         status = 'NOUVEAU',
                         title = message[:100],
                         description = message,
                         author = request.user,
                         sequence = 10,
                         due_date = timezone.now() )

            # sauvegarde
            # task.save()

        except Exception as err:
            messages.add_message(request, messages.INFO, "api err {} data={}".format(err , json_data))
            return JsonResponse({"message": err.message})

        return JsonResponse({"message": request.POST})

    else :
        return JsonResponse({"rien ": request.method})

# api update task
### @api_view(['GET', 'PUT', 'DELETE' ])
def update_ticket(request, task_id, format=None):
    """
    api pour api maj tache
    """
    if request.method == 'PUT':
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            data = json_data
            action = data["action"]
            comment = data["comment"]
            task = Ticket.objects.get(pk=task_id)
            # maj de status par action user
            task.status = action

            if comment :
                task.add_commentaire(comment, action)
            else :
                messages.add_message(request, messages.INFO, "api err pas de commentaire !! {}".format(comment))
            # save
            task.save()

        except Exception as err:
            messages.add_message(request, messages.INFO, "api err {} data={}".format(err.message, json_data))
            return JsonResponse({"message": err.message})

        return JsonResponse({"message": request.POST})

    else :
        return JsonResponse({"rien ": request.method})


# api update suite un drag & move task
### @api_view(['GET', 'PUT', 'DELETE' ])
def move_ticket(request, format=None):
    """
    api update suite un drag & move task
    """
    if request.method == 'PUT':
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            data = json_data
            # messages.add_message(request, messages.INFO, "api move taks {} data={}".format("json", json_data))

            new_start = data["start"]
            end_start = data["end"]
            user_id = data["user_id"]
            task_id = data["task_id"]
            # save
            task = Ticket.objects.get(pk=task_id)
            #
            #task.author = data["user_id"]
            task.start_date = data["start"]
            task.due_date = data["end"]
            # save & commit
            task.save()

        except Exception as err:
            messages.add_message(request, messages.INFO, "api err {} data={}".format(err.message, json_data))
            return JsonResponse({"message": err.message})

    return JsonResponse({"rien ": request.method})


@method_decorator(login_required, 'dispatch')
class TicketListFound(APIView):
    """
    List ticket found
    """

    def get(self, request, search_key, format=None):
        if search_key and request.user.is_superuser:
            tickets = Ticket.objects.filter(
                    Q (title__icontains=search_key)
                    | Q(description__icontains=search_key)
                    | Q(assignee__username__icontains=search_key)
                    | Q(category__title__icontains=search_key)
                    ).order_by("-id")
        elif search_key and search_key == 'all':
            tickets = Ticket.objects.filter(assignee=request.user).order_by("-id")
        elif search_key:
            tickets = Ticket.objects.filter(
                title__icontains=search_key,
                assignee=request.user).order_by("-id")
        else :
            tickets = Ticket.objects.filter(assignee=request.user).order_by("-id")

        #
        serializer = TicketsProjectSerializer(tickets, many=True)

        return Response(serializer.data)




@api_view(['GET', 'PUT', 'DELETE' ])
def ticket_detail(request, pk, format=None):
    """
    api ticket_list s'occupe des demande GET, UPDATE et DELETE
    """

    try :
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET' :
        ticket_serialise = TicketSerializer(ticket)
        return Response(ticket_serialise.data)

    elif request.method == 'PUT':
        ticket_serialise = TicketSerializer (ticket, data=request.data)
        if ticket_serialise.is_valid() :
            ticket_serialise.save()
            return Response(ticket_serialise.data)
        else :
            return Response(ticket_serialise.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@method_decorator(login_required, 'dispatch')
class MesTicketsProjectList(APIView):
    """
    List all ticket of project_id
    """
    def get(self, request, user_id, format=None):
        tickets = Ticket.objects.filter(assignee__id=user_id).all().order_by( '-id', '-urgency', 'status',  )
        serializer =  TicketsProjectSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer =  TicketsProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        messages.add_message(request, messages.INFO, "error api todo delete  {}".format(pk))
        # ticket = self.get_object(pk)
        ticket= Ticket.objects.get(pk=pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator(login_required, 'dispatch')
class TicketsProjectList(APIView):
    """
    List all ticket of project_id
    """
    def get(self, request, project_id, format=None):
        tickets = Project.objects.get(pk=project_id).tickets.all().order_by( '-id', '-urgency', 'status',  )
        serializer =  TicketsProjectSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer =  TicketsProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )


@method_decorator(login_required, 'dispatch')
class ServicesSociete(APIView):
    """
    List all services
    """
    def get(self, request, societe_id, format=None):
        services = Service.objects.get(pk=societe_id).all().order_by( '-name',)
        serializer = ServicesSociete(services, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def ticket_list(request, format=None):
    """
    api ticket_list s'occupe des demande
    LIST & CREATE
    """
    DEFAULT_RENDERER_CLASSES = ('rest_framework.renderers.JSONRender'  , 'rest_framework.renderers.BrowsableAPIRender' )

    if request.method == 'GET' :
        tickets = Ticket.objects.all().order_by('-created')
        ticket_serialise = TicketSerializer(tickets, many=True)
        return Response(ticket_serialise.data)

    elif request.method == 'POST':

        ticket_serialise = TicketSerializer(data=request.data)
        if ticket_serialise.is_valid() :
            messages.add_message(request, messages.INFO, "ticket valide  {}" .format(json.dumps(request.data) ))
            ticket_serialise.save()
            return Response(ticket_serialise.data, status=status.HTTP_201_CREATED)

        else :
            data_json = json.dumps(request.data)
            messages.add_message(request, messages.INFO, "error {} api ticket_list POST no_va {}".format(ticket_serialise.errors, request.data.items()))
            return Response(ticket_serialise.errors , status=status.HTTP_400_BAD_REQUEST)




@method_decorator(login_required, 'dispatch')
#@api_view(['GET', 'PUT', 'DELETE' ])
class TodoTodayList(APIView):
    """
    List all todo
    Retrieve, update or delete a snippet instance.
    curl -X DELETE "http://127.0.0.1:8000/api/vtodo/(?P<pk>[-\d]+)/delete/"
    """
    def get(self, request, user_id, format=None):
        todos = Vtodo.objects.filter(author__id=user_id).all().order_by( '-id' )
        serializer = TodoTodaySerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # serializer
        serializer =  TodoTodaySerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # error !!
        messages.add_message(request, messages.INFO, "error api  TodoTodayList  {}".format(serializer.errors))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        todo = Vtodo.objects.get(pk=pk)
        serializer = TodoTodaySerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # messages.add_message(request, messages.INFO, "error api todo delete  {}".format(pk))
        # todo = self.get_object(pk)
        todo = Vtodo.objects.get(pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
