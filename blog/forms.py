
from mdeditor.fields import MDTextFormField
import blog.models as blog_models
from mdeditor.fields import  MDEditorWidget
author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2019 Strand Cosmetics'
__version__ = '0.9'

import datetime, time, os
from django import forms as forms
from django.utils.translation import ugettext_lazy as _
from core.taxonomy.models import Document

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
                    field.label = _(field.label)  # traduire le label
                # les input

                if type(field.widget) in (forms.TextInput,  forms.EmailField, forms.EmailInput):
                    field.widget.attrs['class'] = 'input-lg'
                    # charger place holder
                    field.widget.attrs['placeholder'] = field.label
                elif type(field.widget) in (forms.Select, forms.SelectMultiple ):
                    field.widget.attrs['class'] = 'input-lg'

                elif type(field.widget) in  (forms.DateInput, forms.DateTimeInput) :
                    field.widget.attrs['class'] = 'form-control input-lg'
                    field.widget.attrs['type'] = "datetime-local"
                    field.widget.attrs['type'] = "datetime"

class BlogForm(BootstrapModelForm):
    content = MDTextFormField ()

    class Meta:
        model = blog_models.Article
        fields =  '__all__'
        exclude = ('created', 'modified',  'tags' )


class DocumentForm(BootstrapModelForm):

    class Meta:
        model = Document
        fields = ( 'document', 'do_title', 'do_description' , 'active')
