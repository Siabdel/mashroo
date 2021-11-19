#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file
This program is appli todo for manage incidents and action
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2019 Strand Cosmetics'
__version__ = '0.9'
from django.db import models
import datetime
from django.db.models import Count, F, Value

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

class TicketManager(models.Manager):
    """Custom manager for Ticket model.
    """
    def opened(self):
        return self.filter(closed=None)

    def closed(self):
        return self.exclude(closed=True)

    def overdue(self):
        return self.filter(due_date__gt=datetime.date.today())

    def nb_users_assignee(self):
        return self.filter(due_date__gt=datetime.date.today(),
                    statut__in=( 'ENCOURS', 'REALISEE', 'NOUVEAU')).values('status', 'assignee').annotate(dcount=Count('assignee'))

    def event_color(self):
        return {
            'NOUVEAU':  YELLOW_CITRON ,
            'ENCOURS': BLUE,
            'RESOLUE': GREEN,
            'CLOTUREE': GREEN_APPLE,
            'ANNULEE': GREY,
            'ENATTENDE': ORANGE,
            }
