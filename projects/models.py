#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage projects
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2019 Strand Cosmetics'
__version__ = '0.9'

from datetime import datetime
from django.utils import timezone

from django.db import models
#from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from mashroo import settings
from projects.managers import TicketManager

from core.utils import assign_code
from core.profile.models import UProfile

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User, Group, Permission
from django.db import models
from taggit.managers import TaggableManager
import pandas as pd

"""
from django.utils import timezone
now_aware = timezone.now()
Vous devez configurer une infrastructure de paramètres Django de base, même si vous utilisez simplement
 ce type d'interface (dans les paramètres, vous devez inclure *** USE_TZ=True  *** pour obtenir une date / heure consciente).
"""

ORANGE  = "#FFA500"
ORANGE  = "#FF7F00"
YELLOW  = "#FFFF00"
RED     = "#FF1111"
YELLOW_CITRON = "#F7FF3C"
GREEN       = "#008000"
GREEN_APPLE = "#8db600"
BLUE        =	"#0000FF"
DARKBLUE    =	"#0000A0"
LIGHTBLUE   =	"#ADD8E6"
PURPLE	    = "#800080"
LIGHT_YELLOW4 = "#FFFF33"
YELLOW	     = "#FFFF00"
DARK_YELLOW1 = "#CCCC00"
DARK_YELLOW2 =	"#999900"
GREY = "#DCDCDC"
WHITE  = "#FFF"

STATUS_MEMBER_CHOICE = [(1, 'active'), (2, 'premium'), ]


class Member(User):
    """A project Member proxy.
    """
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        self._meta.get_field('is_active').verbose_name = _('active?')
        self._meta.get_field('is_staff').verbose_name = _('staff?')
        self._meta.get_field('is_superuser').verbose_name = _('admin?')

    def __unicode__(self):
        return "%s" % self.username


    def _full_name(self):
        return self.get_full_name()
    _full_name.short_description = _('full name')
    full_name = property(_full_name)

    #@models.permalink
    def get_edit_url(self):
        return ('user_edit', (), {"username": self.username})

    #@models.permalink
    def get_delete_url(self):
        return ('user_delete', (), {"username": self.username})


class Partenaire(models.Model):
    tiers_id    = models.CharField(max_length=3)
    tiers_name  = models.CharField(max_length=100)
    tiers_type  = models.CharField(max_length=1, choices=(('C', 'Client'), ('F', 'Fornisseur')), default='C')
    created     = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # Listed below are the mandatory fields for a generic relation
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')


    def __str__(self):
        return "tiers=%s id=%s" % (self.tiers_type , self.tiers_id)

class Project(models.Model):
    """
    Project model
    """
    code    = models.SlugField(max_length=50, verbose_name=_('code'))
    title   = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author      = models.ForeignKey('auth.User', related_name='created_projects', null=True, blank=True, verbose_name=_('created by'), on_delete=models.SET_NULL)
    manager     = models.ForeignKey('auth.User', related_name='managed_projects', null=True, blank=True, verbose_name=_('project manager'), on_delete=models.SET_NULL)
    status      = models.CharField(_('status'), choices= settings.PROJECT_STATUS_CHOICES, default= settings.PROJECT_DEFAULT_STATUS, max_length=10 )
    category    = models.ForeignKey('taxonomy.Category',  null=True, blank=True, verbose_name=_('categories'), related_name='mes_projects', on_delete=models.SET_NULL)
    #tags = GenericRelation(TaggedItem, related_name='projets')
    tags = TaggableManager()
    # dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_('dashboard'))
    stream = models.OneToOneField('notifications.Stream', null=True, blank=True, verbose_name=_('stream'), on_delete=models.SET_NULL)

    participants = models.ManyToManyField(UProfile, through='Membership' , verbose_name=_('Participants'), ) # les participants au prject

    partenaire  = GenericRelation(Partenaire, null=True, blank=True) # clients ou fournisseurs
    documents   = GenericRelation('taxonomy.GDocument',  null=True, blank=True) #  les documents rattachées

    visibilite  = models.CharField(max_length=100, choices=settings.VISIBILITE_CHOICES, default=settings.VISIBILITE_DEFAULT, verbose_name=_('visiblite'))

    created     = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    due_date    = models.DateTimeField(verbose_name=_("date d\'echeance"))
    closed      = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    date_debut  = models.DateTimeField(verbose_name=_('date debut'),  ) # timezone.now()
    date_fin    = models.DateTimeField(verbose_name=_('date debut'), null=True, blank=True)

    comment     = models.TextField(null=True, blank=True)


    class Meta:
        ordering = ['code']
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __unicode__(self):
        return "%s" % self.code

    def save(self):
        if self.status in settings.PROJECT_CLOSE_STATUSES :
            if self.closed is None:
                self.closed = timezone.now()
                # cloturee all task
                try :
                    project_tickets = Ticket.objects.filter(project=self).all()
                    project_tickets.update(status='CLOTUREE')
                except Eception as err:
                    pass

        else:
            self.closed = None

        # super save
        super(Project, self).save()

    def working_hours(self):
        count = 0
        for ticket in self.tickets.all():
            count += ticket.working_hours()
        return count

    @property
    def eventColor(self):
        if self.status == 'NOUVEAU':
            return  YELLOW_CITRON
        elif self.status == 'ENCOURS':
            return BLUE
        elif self.status == 'RESOLUE':
            return  GREEN
        elif self.status == 'CLOTUREE':
            return  GREEN_APPLE
        elif self.status == 'ANNULEE':
            return  GREY
        elif self.status == 'ENATTENDE':
            return  ORANGE
        else :
            return  WHITE




    #@models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {"pk": self.pk})

    #@models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {"pk": self.pk})

    #@models.permalink
    def get_edit_url(self):
        return ('project_edit', (), {"pk": self.pk})

    #@models.permalink
    def get_delete_url(self):
        return ('project_delete', (), {"pk": self.pk})

    def add_tags(self, tag_label):
        """
        b = Bookmark(url='https://www.djangoproject.com/')
        >>> b.save()
        >>> t1 = TaggedItem(content_object=b, tag='django')
        >>> t1.save()
        # les tags de object Bookmark
        tags = GenericRelation(TaggedItem, related_query_name='bookmark')
        # types de recherches manuellement :
        >>> bookmarks = Bookmark.objects.filter(url__contains='django')
        >>> bookmark_type = ContentType.objects.get_for_model(Bookmark)
        >>> TaggedItem.objects.filter(content_type__pk=bookmark_type.id, object_id__in=bookmarks)
        """
        t1 = TaggedItem(content_object=self, object_id=self.pk, tag=tag_label)
        t1.save()

    def get_tag_project(self):
        return TaggedItem.objects.filter(content_type__pk=self.id)

    def add_member(self, member):
        """
        ajout de membre au projet
        """
        if not Membership.objects.filter(project=self, member=member).exists() :
            instance = Membership.objects.create( project = self, member=member)
            instance.save()

    def list_members(self):
        """
        liste des membres du projet
        """
        return  self.participants.all().order_by('user')


    # les tags de object Bookmark
    def get_all_tags_project(self):
        return ContentType.objects.get_for_model(Project)

    # add  partenaire du project
    def add_partenaire_client(self, partenaire_id, partenaire_name, partenaire_type='C'):
        """
        pp1 = models.Project.objects.get(pk=25)
        cli1 = of_models.DjangoClient.objects.get(codeclie=222)
        cli2 = of_models.DjangoClient.objects.get(codeclie=223)
        t1 = models.Partenaire(content_object=pp1, tiers=cli1.codeclie)
        t2 = models.Partenaire(content_object=pp1, tiers=cli2.codeclie)
        t1.save() ; t2.save()
        models.Partenaire.objects.filter(content_type=pp1)
        """

        t1 = Partenaire(content_object=self,
                        tiers_id=partenaire_id,
                        tiers_name=partenaire_name,
                        tiers_type=partenaire_type)
        t1.save()

    # get partenaire du project
    def get_partenaires_project(self):
        return Partenaire.objects.filter(object_id=self.pk)
            ## Upload files

    # add document du project
    def add_document(self, document):
        """
        """
        doc= GDocument(content_object=self, document = document)
        doc.save()

    # get pieces jointes au project
    def get_documents_project(self):
        return self.documents.all()
    # get pieces jointes au project

    def get_images_project(self):
        images = []
        for elem in self.documents.all():
            if os.path.exists(elem.document.document.path) :
                if elem.document.file_type in  ('jpeg',  'jpg' , 'png' ,  'gif'):
                    images.append(elem)
        return images

    def get_image_active(self):
        for photo in self.documents.all():
            if photo.document.active == True:
                return photo
        return None



    @property
    def progress(self):
        total = Ticket.objects.filter(project = self.project).count()
        if total > 0:
            closed = Ticket.objects.filter(project = self.project, closed=True).count()
            return int(closed / float(total) * 100)
        return 100


# M2M entre Project et UProfile
class Membership(models.Model):
    member = models.ForeignKey(UProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    invite_reason = models.CharField(max_length=64)


##  les petits pas
class MilestoneAdmin(models.Model) :

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        assign_code(self)

    def __unicode__(self):
        return u'#%s %s' % (self.code, self.title)

    #@models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {"pk": self.pk})

    #@models.permalink
    def get_edit_url(self):
        return ('project_edit', (), {"pk": self.pk})

    #@models.permalink
    def get_delete_url(self):
        return ('project_delete', (), {"pk": self.pk})

    def save(self):
        if self.status in settings.PROJECT_CLOSE_STATUSES:
            if self.closed is None:
                self.closed = timezone.now()
        else:
            self.closed = None
        super(Project, self).save()

    def working_hours(self):
        count = 0
        for ticket in self.tickets.all():
            count += ticket.working_hours()
        return count


class Milestone(models.Model):
    """Milestone model. un jalon qui signal la fin d'une etape
    """
    code = models.SlugField(max_length=100, verbose_name=_('code'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    project = models.ForeignKey(Project, verbose_name=_('project'), on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User',  related_name='created_milestones',    verbose_name=_('created by'), on_delete=models.CASCADE)
    manager = models.ForeignKey('auth.User', related_name='managed_milestones', null=True, blank=True, verbose_name=_('manager'), on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('deadline'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category',  blank=True, verbose_name=_('categories'))

    # tags = models.ManyToManyField('taxonomy.Tag',   blank=True, verbose_name=_('tags'))
    tags = GenericRelation('taxonomy.TaggedItem')

    # dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_('dashboard'))
    # stream = models.OneToOneField('notifications.Stream', null=True, verbose_name=_('stream'))
    # members = models.ManyToManyField(Member, through='Milestone_Member', verbose_name=_('Paritcipants action')) # les participants au prject



    class Meta:
        ordering = ['project', 'deadline', 'code']
        verbose_name = _('milestone')
        verbose_name_plural = _('milestones')

    def __init__(self, *args, **kwargs):
        super(Milestone, self).__init__(*args, **kwargs)
        assign_code(self)

    def __unicode__(self):
        return u'#%s %s' % (self.code)

    def _expired(self):
        if self.deadline:
            if self.closed:
                return self.closed > self.deadline
            else:
                return timezone.now() > self.deadline
        return False
    expired = property(_expired)

    def _progress(self):
        total = self.tickets.count()
        if total > 0:
            closed = self.tickets.closed().count()
            return int(closed / float(total) * 100)
        return 100
    progress = property(_progress)

    #@models.permalink
    def get_absolute_url(self):
        return ('milestone_detail', (), {"project": self.project.code, "code": self.code})

    #@models.permalink
    def get_edit_url(self):
        return ('milestone_edit', (), {"project": self.project.code, "code": self.code})

    #@models.permalink
    def get_delete_url(self):
        return ('milestone_delete', (), {"project": self.project.code, "code": self.code})

    def working_hours(self):
        count = 0
        for ticket in self.tickets.all():
            count += ticket.working_hours()
        return count



class Ticket(models.Model):
    """
    Ticket model. Incident
    """
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',  on_delete=models.SET_NULL)

    project = models.ForeignKey(Project, related_name='tickets', verbose_name=_('project'), on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField(verbose_name=_('sequence'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(help_text=_('Use <a href="http://daringfireball.net/projects/markdown/syntax">MarkDown syntax</a>.'), verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name="created_tickets", verbose_name=_('created by'), on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=settings.TASK_TYPE_CHOICES, default=settings.TASK_DEFAULT_TYPE, verbose_name=_('type'))
    urgency = models.CharField(max_length=20, choices=settings.TICKET_URGENCY_CHOICES, default=settings.TICKET_DEFAULT_URGENCY, verbose_name=_('urgency'))
    status = models.CharField(max_length=20, choices=settings.TICKET_STATUS_CHOICES, default=settings.TICKET_DEFAULT_STATUS, verbose_name=_('status'))
    assignee = models.ForeignKey('auth.User', related_name="assigned_tickets", null=True, blank=True, verbose_name=_('assigned to'), on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    category  = models.ForeignKey('taxonomy.Category',  null=True, blank=True, verbose_name=_('categorie'), related_name='mes_tickets', on_delete=models.SET_NULL)

    # tags = models.ManyToManyField('taxonomy.Tag',   blank=True, verbose_name=_('tags'))
    due_date        = models.DateTimeField(null=True, blank=True)   # date d'echeance - deadline
    start_date      = models.DateTimeField(null=True, blank=True) # date debut de realisation
    end_date        = models.DateTimeField(null=True, blank=True) # date de fin de realisation
    schedule_date   = models.DateTimeField(null=True, blank=True) # date planifiee

    tags = TaggableManager()

    tasks   = models.ManyToManyField('todo.Task', blank=True, verbose_name=_('related tasks'))
    stream  = models.OneToOneField('notifications.Stream', null=True, verbose_name=_('stream'),on_delete=models.SET_NULL)
    comments   = GenericRelation('taxonomy.Commentaire', null=True, blank=True) #  les commantaires rattachées
    documents  = GenericRelation('taxonomy.GDocument', null=True, blank=True) #  les documents rattachées

    objects = TicketManager()

    class Meta:
        ordering = ('project', '-sequence')
        permissions = [ ("change_assignee", "Can change assignee"), ]
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __init__(self, *args, **kwargs):
        super(Ticket, self).__init__(*args, **kwargs)
        if not self.sequence:
            uid = 1
            try:
                last_ticket = Ticket.objects.filter(project=self.project).latest('created')
                uid = int(last_ticket.code) + 1
            except:
                pass
            self.code = uid

    def __unicode__(self):
        return u'#%d %s' % (self.sequence, self.title)

    #@models.permalink
    def get_absolute_url(self):
        return ('ticket_detail', (), {   "pk" : self.pk})

    #@models.permalink
    def get_edit_url(self):
        return ('ticket_edit', (),    { "project" : self.project.pk,  "pk" : self.pk})

    #@models.permalink
    def get_delete_url(self):
        return ('ticket_delete', (),  { "project" : self.project.pk,  "pk" : self.pk})

    # add  partenaire du project
    def add_commentaire(self, content_comment, v_action):
        """
        """
        comment = Commentaire(description=content_comment,
                              content_object=self,
                              user_assignee=self.assignee,
                              current_status = v_action,
                              object_id=self.pk)
        comment.save()

    # get partenaire du project
    def get_commentaires(self):
        return Commentaire.objects.filter(object_id=self.pk)

    # add document du project
    def add_document(self, document):
        """
        """
        doc= GDocument(content_object=self, document = document)
        doc.save()

    # get pieces jointes au project
    def get_documents_project(self):
        return self.documents.all()


    def save(self, *args, **kwargs):
        if self.status in settings.TICKET_CLOSE_STATUSES: # CLOTUREE ou ANNULEE
            if self.closed is None:
                self.closed = timezone.now()
                self.end_date = timezone.now()

        if self.status in 'NOUVEAU':
            self.start_date = None
            self.end_date = None
            self.closed = None

        if self.status in 'ENCOURS':
            if not self.start_date  :
                self.start_date = timezone.now()

        if self.status in 'RESOLUE':
            if self.end_date is None:
                self.end_date = timezone.now()

        if self.status in 'CLOTUREE':
            if self.closed is None:
                self.closed = timezone.now()

        if not self.author :
            self.author = self.request.user

        # save & coherence de dates
        if not self.schedule_date :
            self.schedule_date = self.project.date_debut

        if (self.schedule_date and  self.project.date_debut):
            if self.schedule_date < self.project.date_debut :
                self.schedule_date = self.project.date_debut

        if (self.due_date and self.schedule_date) :
            if self.schedule_date > self.due_date :
                self.schedule_date = self.project.date_debut
        # save
        # raise Exception("erreur : %s" % self.project.pk)
        return super(Ticket, self).save( *args, **kwargs)
        # save ManyToManyField Ticket_Projet
    @property
    def is_manager(self):
        return self.project.manager == self.author

    @property
    def is_assignee(self, user_connecter):
            if self.assignee == user_connecter:
                return True
    @property
    def working_hours(self):
        count = 0
        for task in self.tasks.all():
            count += task.working_hours()
        return count


    def add_tags(self, tag_label):
        """
        b = Bookmark(url='https://www.djangoproject.com/')
        >>> b.save()
        >>> t1 = TaggedItem(content_object=b, tag='django')
        >>> t1.save()
        # les tags de object Bookmark
        tags = GenericRelation(TaggedItem, related_query_name='bookmark')
        # types de recherches manuellement :
        >>> bookmarks = Bookmark.objects.filter(url__contains='django')
        >>> bookmark_type = ContentType.objects.get_for_model(Bookmark)
        >>> TaggedItem.objects.filter(content_type__pk=bookmark_type.id, object_id__in=bookmarks)
        """
        t1 = TaggedItem(content_object=self, tag=tag_label)
        t1.save()

    @property
    def delai_due_date(self):
        aujourdhui = timezone.now()
        if self.due_date :
            # return  (aujourdhui - self.due_date ).days
            jours_ouvrable = len(pd.bdate_range( aujourdhui.strftime("%Y-%m-%d") , self.due_date.strftime("%Y-%m-%d") ))
            return -jours_ouvrable
        else :
            return False


    def get_jours_ouvrable(self, date1, date2):
        """
        pd.bdate_range( date_debut, date_fin ) permet de calculer
        les jours ovrable entre 2 dates
        input :: str : date1,
        input :: str : date2
        return :: retour pandas datatype liste de date vacances pour ces 2 ans
        """
        aujourdhui = datetime.timezone.now()
        date_debut  = str(date1)
        date_fin    = str(date2)
        return pd.bdate_range( date_debut, date_fin )

    def get_jours_vacance(self, annees=[]):
        """
        input :: annee
        return :: retour la liste de date vacances pour cette annee
        """
        fr_vacances = []
        if len(annees) > 0 :
            for vacance in holidays.France(years=annees).items():
                fr_vacances.append(str(vacance[0]))
        return fr_vacances


    @property
    def nbjours_ouvrable_due_date(self):
        """
        return : delai qui reprente les jours ouvrables en excluant les jour de vacances française
        """
        aujourdhui = timezone.now()
        date1 = aujourdhui.strftime("%Y-%m-%d")
        date2 = self.due_date.strftime("%Y-%m-%d")

        date_ouvrables = self.get_jours_ouvrable(date1, date2)
        # dd = [ 1 if str(val).split()[0] in fr_vacances else 0 for val in date_ouvrables ]
        #
        pf = pd.DataFrame(data=date_ouvrables, columns=['jours_ouvrable'])
        #
        # les jour de vacance dans cette echantillons de jours_ouvrable
        date_vacances = self.get_jours_vacance([int(date1), int(date2)])
        pf['holiday'] = pd.DataFrame(data=date_vacances)
        #
        list_jours_vacances   = [ elem for elem in  pf['holiday'].values if type(elem) == str ]
        list_jours_ouvrable   = [ elem.strftime('%Y-%m-%d') for elem in pf['jours_ouvrable']  ]
        #
        jours_ouvrable_exclude_vacances = [ elem for elem in list_jours_ouvrable if elem not in list_jours_vacances]
        return 999

    @property
    def delai_planifie(self):
        aujourdhui = timezone.now()
        if self.due_date and self.schedule_date:
            jours_ouvrable = len(pd.bdate_range( self.schedule_date.strftime("%Y-%m-%d") , self.due_date.strftime("%Y-%m-%d") ))
            # return  (aujourdhui - self.due_date ).days
            return -jours_ouvrable
        else :
            return False

    @property
    def delai_closed_date(self):
        aujourdhui = timezone.now()
        if self.closed and self.start_date  :
            if (self.closed - self.start_date ).days == 0:
                return (self.start_date - self.closed ).days
            else :
                return  (self.closed - self.start_date ).days
        else :
            return False

    def delai_realisation(self):
        aujourdhui = timezone.now()
        if self.end_date and self.start_date  :
            if (self.end_date - self.start_date ).days == 0:
                return (self.end_date.hour - self.start_date.hour )
            else :
                return  (self.end_date - self.start_date).days
        else :
            return False


    @property
    def start(self):
        return self.start_date

    @property
    def end(self):
        return self.end_date

    @property
    def resourceId(self):
        return self.project.pk

    @property
    def eventColor(self):
        """
        """
        if self.status == 'NOUVEAU':
            return  YELLOW_CITRON
        elif self.status == 'ENCOURS':
            return ORANGE
        elif self.status == 'RESOLUE':
            return  GREEN
        elif self.status == 'CLOTUREE':
            return  GREEN_APPLE
        elif self.status == 'ANNULEE':
            return  GREY
        elif self.status == 'ENATTENTE':
            return  LIGHTBLUE
        else :
            return  WHITE

    @property
    def urgencyColor(self):
        """
        """
        if self.urgency == 'URGENT' : # important et     urgent
            return RED
        elif self.urgency == 'CRITIQUE': # important et peu urgent
            return  ORANGE
        elif self.urgency == 'FAIBLE' :
            return  GREEN
        elif self.urgency == 'MOYEN' :
            return YELLOW
        else :
            return  WHITE


    @property
    def expired(self):
        if self.due_date :
            if self.closed:
                return self.closed > self.due_date
            else:
                return timezone.now() > self.due_date
        return False

#---------------------------------
# model pour API component  todo
#---------------------------------
class Vtodo(models.Model):
    """
    Vtodo model. VTODO
    """
    title = models.CharField(max_length=255, verbose_name=_('title'))
    author = models.ForeignKey('auth.User', related_name="created_toto", verbose_name=_('created by'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    completed = models.BooleanField(default=False)
    active = models.BooleanField(default=False)


#------------------------
# class client
#------------------------
class DjangoClient (models.Model):
    codeclie = models.CharField(max_length=3,  primary_key=True) # code client
    nomclie = models.CharField(max_length=45) # nom client
    codpost = models.CharField(max_length=5, null=True, blank=True)
    ville   = models.CharField(max_length=20, null=True, blank=True)
    phone   = models.CharField(max_length=15, null=True, blank=True)
    pays    = models.CharField(max_length=20, null=True, blank=True)
    exig_pharma = models.BooleanField(default=False)         # exigences pharmacuetique

    class Meta:
        managed  = True

    def __unicode__(self):
        return u'%s'.format( self.nomclie)
