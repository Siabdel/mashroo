#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2019 Strand Cosmetics'
__version__ = '0.9'


from django.forms.fields import *
from django.forms.widgets import *
from django import forms
# from core.forms.fields import *
# from core.forms.widgets import *

from models import *
from core.forms.widgets import CKEditor, SelectMultipleAndAddWidget

class TaskForm(forms.ModelForm):
    """Form for Task data.
    """
    start = DateTimeField(required=False)
    end = DateTimeField(required=False)

    class Meta:
        model = Task
        exclude = ('user', 'closed')
        widgets = {
            'description': CKEditor(),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

# enrich_form(TaskForm)
