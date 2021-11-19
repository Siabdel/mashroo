#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2019 Strand Cosmetics'
__version__ = '0.9'

from datetime import datetime, timedelta

from django.db import models
#from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class Task(models.Model):
    """
    Task model.
    """
    title       = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    user        = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_('proprietaire'), on_delete=models.SET_NULL)
    start       = models.DateTimeField(null=True, blank=True, verbose_name=_('date debut'))
    end         = models.DateTimeField(null=True, blank=True, verbose_name=_('date fin'), default=timezone.now)
    created     = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    closed      = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories  = models.ForeignKey('Category', null=True, blank=True, verbose_name=_('categories'), on_delete=models.SET_NULL)
    tags        = models.ManyToManyField('Tag', blank=True, verbose_name=_('tags'))

    class Meta:
        ordering = ('-start',)
        get_latest_by = '-start'
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __unicode__(self):
        return u'%s' % self.title

    #@models.permalink
    def get_absolute_url(self):
        # return ('task_detail', (), {"id": self.pk})
        return reverse('task_detail', kwargs={'pk': self.pk})

    #@models.permalink
    def get_edit_url(self):
        return reverse('task_edit', kwargs={"id": self.pk})

    #@models.permalink
    def get_delete_url(self):
        return reverse('task_delete', kwargs={"id": self.pk})

    def save(self):
        if self.start and not self.end:
            self.end = self.start + timedelta(hours=1)
        super(Task, self).save()

    def planned(self):
        return (self.start is not None)

    def started(self):
        return (self.start <= datetime.now())

    def expired(self):
        if self.end:
            return (self.end < datetime.now())
        else :
            return False

    def working_hours(self):
        count = 0
        entries = self.timesheetentry_set.all()
        if entries:
            for entry in self.timesheetentry_set.all():
                count += entry.working_hours()
        elif self.planned():
            td = self.end - self.start
            count = (td.seconds + td.days * 24 * 3600) / 3600
        elif self.closed:
            td = self.closed - self.created
            count = (td.seconds + td.days * 24 * 3600) / 3600
        return count


class Tag(models.Model):
    """
    Tag model.
    """
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    def _occurences(self):
        object_list = []
        related_objects = self._meta.get_all_related_many_to_many_objects()
        for related in related_objects:
            if related.opts.installed:
                model = related.model
                for obj in model.objects.select_related().filter(tags__title=self.title):
                    object_list.append(obj)
        return object_list
    occurences = property(_occurences)

    #@models.permalink
    def get_absolute_url(self):
        return ("tag_detail", (), {"slug": self.slug})


class Category(models.Model):

    """Category model.
    """
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def _occurences(self):
        object_list = []
        related_objects = self._meta.get_all_related_many_to_many_objects()
        for related in related_objects:
            if related.opts.installed:
                model = related.model
                for obj in model.objects.select_related().filter(categories__title=self.title):
                    object_list.append(obj)
        return object_list
    occurences = property(_occurences)

    def __unicode__(self):
        return u'%s' % self.title

    #@models.permalink
    def get_absolute_url(self):
        return ("category_detail", (), {"slug": self.slug})
