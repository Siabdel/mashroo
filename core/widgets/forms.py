#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.5'

from django import forms

from  core.forms import enrich_form
from  core.forms.widgets import JsonPairWidget

from core.widgets.models import *
from core.widgets.loading import registry

class WidgetTemplateForm(forms.ModelForm):
    """Form for widget template data.
    """
    class Meta:
        model = WidgetTemplate
        fields = '__all__'
        widgets = {'context': JsonPairWidget(), 'source': forms.Select()}

    def __init__(self, *args, **kwargs):
        super(WidgetTemplateForm, self).__init__(*args, **kwargs)
        self.fields['source'].widget.choices = registry.sources

class WidgetForm(forms.ModelForm):
    """Form for widget data.
    """
    class Meta:
        model = Widget
        exclude = ['region', 'slug', 'show_title', 'editable', 'sort_order']
        widgets = {'context': JsonPairWidget()}

    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)
        self.fields['template'].queryset = WidgetTemplate.objects.filter(public=True)

enrich_form(WidgetForm)
enrich_form(WidgetTemplateForm)
