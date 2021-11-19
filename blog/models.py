#-----------------------------
# class Blog
#-----------------------------

from django.db import models
from mdeditor.fields import MDTextField,  MDEditorWidget
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User, Group, Permission
from django.db import models
from taggit.managers import TaggableManager
import pandas as pd

class Article(models.Model):
    title = models.CharField(max_length=120)
    recap = models.CharField(max_length=500, default="")
    content = MDTextField()
    author = models.ForeignKey('auth.User', related_name="created_by", verbose_name=_('created by'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified on'))
    active = models.BooleanField(default=False)
    comments   = GenericRelation('taxonomy.Commentaire', null=True, blank=True) #  les commantaires rattachées
    documents  = GenericRelation('taxonomy.GDocument', null=True, blank=True) #  les documents rattachées
    category   = models.ForeignKey('taxonomy.Category',  null=True, blank=True, verbose_name=_('categories'), related_name='mes_article', on_delete=models.SET_NULL)
    tags = TaggableManager()

    class Meta:
        ordering = ('created', 'title')
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


    def __unicode__(self):
        return u'#%d %s' % (self.title)

    #@models.permalink
    def get_absolute_url(self):
        return ('artilce_details', (), {   "pk" : self.pk})

    #@models.permalink
    def get_edit_url(self):
        return ('article_edit', (),    {  "pk" : self.pk})

    #@models.permalink
    def get_delete_url(self):
        return ('article_delete', (),  {  "pk" : self.pk})

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
    def get_documents_article(self):
        return self.documents.all()
