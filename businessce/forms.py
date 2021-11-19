# -*- coding:UTF-8 -*-
import re
import datetime
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms.utils import ErrorList, ValidationError, ErrorDict
from businessce import models
# translate
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.models import inlineformset_factory

DURATION_WIDGET_OPTIONS = {
    'format': 'hh:ii',
    'minuteStep': 15,
}
#--------------------------
w_titre = forms.TextInput(attrs={'size': 100, 'class': 'form-control'})
w_slug = forms.TextInput(attrs={'size': 50,  'class': 'form-control'})
text_widget = forms.TextInput(attrs={'size': 40, 'class': 'form-control'})
contenu_widget = forms.Textarea(
    attrs={'cols': 80, 'rows': 12, 'class': 'form-control'})
w_radio_select = forms.RadioSelect(attrs={'class': 'radio'})


semaine_aujourdhui = datetime.datetime.isocalendar(datetime.datetime.now())[1]
SEMAINES_CHOICE = [(sem, sem) for sem in range(semaine_aujourdhui, 53, 1)]
# -- formulaire de recherche Medecin
JOURS_SEMAINE = [(1, 'lundi'), (2, 'mardi', ), (3, 'mercredi'),
                 (4, 'jeudi'),  (5, 'vendredi'), (7, 'samedi')]


#---------------------------------
# validation de champ telephone
#---------------------------------
def format_validator(value):
    if not re.match("([a-z]+[ ]*[,][ ]*)+([a-z]+[ ]*)$", value):
        raise ValidationError(u'mauvais format saisie !!')

def format_validator_semaine(value):
    if not re.match("([\d]{2})$", value):
        raise ValidationError(u'mauvais samine saisie !!')



# ------------------------------------
# -- formulaire de recherche Medecin
# ------------------------------------
class SearchForm(forms.Form):

    cle_recherche = forms.CharField(max_length=50,
                widget=forms.TextInput(attrs={'size': 60}))

    def __init__(self, *args, **kwargs):
        # appel a la class mère
        super(SearchForm, self).__init__(*args, **kwargs)
        # charger les parametre semaine et annee
        for key, field in self.fields.items():
            if field:
                field.widget.attrs['class'] = 'form-control'
                if field.label:
                    field.label = ugettext(field.label)  # traduire le label
                # les input
                if type(field.widget) in (forms.Select, forms.TextInput,
                                          forms.SelectMultiple,
                                          forms.DateInput):
                    field.widget.attrs['class'] = 'input-lg'
                    # charger place holder
                    field.widget.attrs['placeholder'] = field.label
