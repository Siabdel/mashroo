# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from todo import models

# Register your models here.

#-----------------
# Project
# ---------------

class TodoAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.Tag._meta.get_fields()]
    # list_total.remove('tags')

    list_display = list_total
    #list_display = ['id',   ]


class TaskAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  models.Task._meta.get_fields()]
    # list_total.remove('tags')
    list_total.remove('tags')

    list_display = list_total
    #list_display = ['id',   ]

class CategoryAdmin(admin.ModelAdmin) :
    list_total  = [f.name for f in  models.Category._meta.get_fields()]
    # list_total.remove('tags')
    #list_display = list_total
    list_display = ['title', 'slug']

admin.site.register(models.Tag, TodoAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Category, CategoryAdmin)
