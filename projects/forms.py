#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2019 Strand Cosmetics'
__version__ = '0.9'

import datetime, time, os
from django import forms
from django.utils.translation import ugettext_lazy as _

from projects.models import Project, Ticket, Milestone, Member, UProfile
from core.taxonomy.models import Category
from core.forms.widgets import CKEditor, SelectMultipleAndAddWidget
from core.forms import enrich_form
from django.contrib.auth.models import User, Group, Permission
from projects.models import DjangoClient
from django.forms import DateTimeInput
from mashroo import settings
from projects import models as pro_models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.models import inlineformset_factory
from core.profile.models import UProfile, Societe, Service
from datetimepicker.widgets import DateTimePicker
from core.taxonomy.models import GDocument, Document

w_titre = forms.TextInput(attrs={'size': 100, 'class': 'form-control'})
w_slug = forms.TextInput(attrs={'size': 50,  'class': 'form-control'})
text_widget = forms.TextInput(attrs={'size': 40, 'class': 'form-control'})
contenu_widget = forms.Textarea(
    attrs={'cols': 80, 'rows': 12, 'class': 'form-control'})
w_radio_select = forms.RadioSelect(attrs={'class': 'radio'})


semaine_aujourdhui = datetime.datetime.isocalendar(datetime.datetime.now())[1]
SEMAINES_CHOICE = [(sem, sem) for sem in range(semaine_aujourdhui, 53, 1)]



## form load Files
class BootstrapModelForm(forms.ModelForm) :

    def __init__(self,  *args, **kwargs):
        # appel a la class mère
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        # set the user_id as an attribute of the form
        #self.fields['semaine'].initial = 33

        # charger la class bootstrap
        for key, field in self.fields.items():
            if field:
                if field.label:
                    field.label = ugettext(field.label)  # traduire le label
                # les input

                if type(field.widget) in (forms.TextInput,  forms.EmailField, forms.EmailInput):
                    field.widget.attrs['class'] = 'input-lg'
                    # charger place holder
                    field.widget.attrs['placeholder'] = field.label

                elif type(field.widget) in (forms.Select, forms.SelectMultiple ):
                    field.widget.attrs['class'] = 'input-lg'

                elif type(field ) in  (forms.DateTimeInput, ) :
                    field.widget.attrs['class'] = 'form-control input-lg'

                elif type(field.widget) in  ( forms.DateTimeInput,  MyDateTimeInput) :
                    field.widget.attrs['class'] = 'form-control input-lg'

        def clean(self, *args, **kwargs):
            data = super(DocumentForm, self).clean(*args, **kwargs)
            filename = os.path.splitext(data)
            data.name = unicode(data.name)
            if len(filename[1]):
                data.name += u'.'+slugify(filename[1])
            return data


class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = 'projects/widgets/bootstrap_datetimepicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input input-lg'
        context = super(BootstrapDateTimePickerInput, self).get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        return context


class MyDateInput(forms.DateInput):
    input_type = 'datet'

class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class ProjectForm(BootstrapModelForm):
    """Form for project data.
    """
    # title = forms.CharField(widget=forms.Select( choices=title_CHOICE), required=True)
    """
    code = forms.CharField(max_length=20)
    code.widget.attrs.update({  'readonly':'true'})
    # author = forms.CharField(widget=forms.HiddenInput(), max_length=20)
    query_responsables  =  User.objects.all().values_list( 'id', 'username' ).order_by('username')
    responsable_choice  = [ (id, username[:20]) for (id,  username) in query_responsables.iterator() ]

    # manager = forms.MultipleChoiceField(label='Résponsable', choices=responsable_choice, required=False)


         #
    description  = forms.CharField(widget = contenu_widget, required=False)
    description.widget.attrs.update({'class': 'input-lg', 'cols':'40', 'rows':'3'})
    # categories_choice   = [ (cat.id, cat) for cat in Category.objects.all().order_by('slug')]
    """

    clients = forms.ChoiceField(label='Partenaires', choices=[], required=False)

    class Meta:
        model = Project
        exclude = ('author', 'closed', 'dashboard', 'stream', 'participants',  'tags', 'date_fin' )
        # fields = ['date_debut']
        widgets = {
                   'date_debut__': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                   'due_date' : DateTimePicker(attrs={'type': 'datetime-local'}),
                   'date_debut_': forms.DateInput(attrs={'type': 'date'})
                    }

        widgets__ = {
            'description': CKEditor(),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

    def __init__(self,  *args, **kwargs):
        # appel a la class mère
        super(ProjectForm, self).__init__(*args, **kwargs)
        #self.fields['category'].evalua299ted_queryset = categories
        # set the user_id as an attribute of the form
        #self.fields['author'].widget = forms.HiddenInput()
        self.fields['code'].widget.attrs.update({  'readonly':'true'})
        # numero de la semaine
        semaine_aujourdhui = datetime.datetime.isocalendar( datetime.datetime.now())
        aujourdhui = datetime.datetime.now()
        self.fields['code'].initial = aujourdhui.strftime("%Y") +  "-" + str(time.time()).replace('.', '-')[4:]
        # self.fields["date_debut"].initial = aujourdhui.strftime('%Y/%m/%d %H:%M')
        # les partenaires
        query_partenaires   =  DjangoClient.objects.all().values_list( 'codeclie', 'nomclie' ).order_by('nomclie')
        partenaires_choice  = [ (codeclie, nomclie[:20]) for ( codeclie, nomclie) in query_partenaires.iterator() ]
        #
        self.fields['clients'].choices = partenaires_choice
        self.fields['due_date'].widget.attrs.update({  'type':'datetime-local'})
        self.fields['comment'].widget.attrs['placeholder'] = "Saisir un commentaire!"
        # date debut le format valide
        ## DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])
        # self.fields['date_debut']  = forms.DateTimeField(widget = forms.SelectDateWidget(), input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M",] )
        self.fields['date_debut']  = forms.DateTimeField(widget = MyDateTimeInput(), input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M",] )
        self.fields['date_debut'].widget.attrs['class'] = 'form-control input-lg'
        ##
        self.fields['due_date']  = forms.DateTimeField(widget = MyDateTimeInput(), input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M",] )
        self.fields['due_date'].widget.attrs.update({'class': 'form-control input-lg'})


    def is_valid__(self):
        # self.data._mutable = True
        # self.data.update({'date_debut': datetime.datetime.strptime(self.data['data_debut'], "%Y-%m-%dT%H:%M")})
        return super(ProjectForm, self).is_valid()

    def save(self, commit=False):
        #
        instance = super(ProjectForm, self).save(commit=False)
        if instance.description == "" :
            instance.description = instance.title
        instance.save()
        return instance


# form des
class MemberProjectForm(forms.ModelForm):

    class Meta :
        model =  UProfile
        exclude = ('project',  )


class MilestoneForm(BootstrapModelForm):
    # Form for milestone data.
    deadline = forms.DateTimeField(required=False)

    class Meta:
        model = Milestone
        exclude = ('project', 'author', 'closed', 'dashboard', 'stream')
        widgets = {
            'description': CKEditor(),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }



class TicketForm(BootstrapModelForm):
    """Form for ticket data.
    """
    class Meta:
        model = Ticket
        exclude = (   'closed', 'stream' , 'tags', 'tasks',  'start_date', 'end_date', 'created')
        widgets = {
            'tasks': SelectMultipleAndAddWidget(add_url='/tasks/add/', with_perms=['todo.add_task']),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        if self.instance is None or self.instance.pk is None:
            del self.fields['status']
        # mettre en hidden ces 3 champs
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['project'].widget = forms.HiddenInput()
        self.fields['sequence'].widget = forms.HiddenInput()
        # self.fields['milestone'].queryset = self.instance.project.milestone_set.all()
        # charger la class bootstrap

        self.fields['schedule_date']  = forms.DateTimeField(widget = MyDateTimeInput(), input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M",] )
        self.fields['schedule_date'].widget.attrs.update({'class': 'form-control input-lg'})

        self.fields['due_date']  = forms.DateTimeField(widget = MyDateTimeInput(), input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M",] )
        self.fields['due_date'].widget.attrs.update({'class': 'form-control input-lg'})

    def save(self, commit=False):
        #
        instance = super(TicketForm, self).save(commit=False)
        if instance.description == "" :
            instance.description = instance.title
        instance.save()
        return instance


enrich_form(ProjectForm)
# enrich_form(MilestoneForm)
enrich_form(TicketForm)



class DocumentForm(BootstrapModelForm):

    class Meta:
        model = Document
        exclude = (  'do_title', 'do_description'  )
        # fields = ( 'document', 'do_title', 'do_description' , 'active')


# form des
class ProfileForm(BootstrapModelForm):
    del_photo = forms.CharField( widget=forms.CheckboxInput(), required=False)
    societe   = forms.CharField(widget=forms.Select(choices=[]), required=True) #  initial='1',
    email     = forms.EmailField(label="Email", required=False) #

    class Meta :
        model =  UProfile
        exclude = ('id', 'user' )

    def __init__(self,  *args, **kwargs):
        # appel a la class mère
        super(ProfileForm, self).__init__(*args, **kwargs)
        query_societe = Societe.objects.all().values_list( 'id', 'name' ).order_by('name')
        societes_choice  = [ (id, name[:20]) for ( id, name) in query_societe.iterator() ]
        self.fields['societe'].widget.choices = societes_choice
        #
        """
        query_service = Service.objects.filter(societe=1).values_list( 'id', 'name' ).order_by('name')
        services_choice  = [ (id, name[:20]) for ( id, name) in query_service.iterator() ]
        self.fields['service'].widget.choices = services_choice
        """
