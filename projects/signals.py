#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

__author__ = 'Abdelaziz Sadquaoui <siabdel@gmail.com>'
__copyright__ = 'Copyright (c) 2019 STRAND COSMETICS EUROPE'
__version__ = '0.0.5'

import django.dispatch
from django.db import models
from django.utils.translation import ugettext_noop as _
from django.core.mail import EmailMessage
# from django.contrib.auth.models import User
#from django.contrib.comments.models import Comment
from django.conf import settings

from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.auth.models import MyPermission, ObjectPermission
# from core.auth.cache import LoggedInUserCache

from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpRequest
from django.shortcuts import render_to_response, get_object_or_404, render, render_to_response, HttpResponseRedirect, reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from projects.utils import send_html_email
from projects.models import Ticket
from django.contrib import messages
## import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


request = HttpRequest()

# request.session.session_key
# sessionid  = cache.get(sessionid)

def send_notification_email(sender, instance, signal, *args, **kwargs):
    if Subscription.objects.filter(signature=instance.signature, user=instance.user, send_email=True).count() > 0:
        email_subject = instance.title
        email_body = instance.description
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost.com')
        email = EmailMessage(email_subject, email_body, email_from, [instance.user.email,])
        email.content_subtype = "html"
        email.send()

## SIGNALS ##

post_change = django.dispatch.Signal(providing_args=["instance", "changes"])
stream_attach = django.dispatch.Signal(providing_args=["instance", "stream"])

## CONNECTIONS ##

# models.signals.post_save.connect(update_user_permissions, sender=User, dispatch_uid="update_user_permissions")
# models.signals.m2m_changed.connect(forward_activity, sender=Activity.streams.through, dispatch_uid="forward_activities")
# models.signals.post_delete.connect(notify_comment_deleted, Comment, dispatch_uid="comment_deleted")


@receiver([post_save, ], sender=Ticket)
def send_mail_handler(sender, **kwargs):
    # on reupère l'instance
    ticket = kwargs["instance"]
    # request = kwargs["request"]

    sujet = u'Project Sce Send email : Your ticket has been registered.......'
    text_content = u" Un ticket vous est assigné comme action a faire. suivre ce lien"

    if kwargs["created"]:

        html_content = "<p> Un ticket vous est assigne comme action a faire. suivre ce lien  <br>  <strong> task here ... </strong> <a href='#' > ICI </a> </p>"
        TO_USERS = [ ticket.author.email, ticket.assignee.email ]
        #TICKET_URL =  "http://" + request.get_host() + reverse('ticket_detail', kwargs={'pk' : ticket.id})
        TICKET_URL =  "http://odysee:90"  + reverse('ticket_detail', kwargs={'pk' : ticket.id})

        message = "test envoie par signal ticket id = {} object = {}, kwargs = {}".format(ticket.id, ticket.title, kwargs)
        context = {
                    'object' : ticket,
                    'url_task' : TICKET_URL,
                    'subject' : sujet,
                    'message' : message,
                }
        try :
            send_html_email(sujet, text_content, TO_USERS, TICKET_URL, context)

        except Exception as err :
            # Log an error message
            msg = 'Erreur send email .. {}!'.format(err)
            logger.error(msg)
            #raise 



# post_save.connect(send_mail_handler, sender=Ticket)
