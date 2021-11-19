# -*- coding: utf-8 -*-
# Extension of http://www.yilmazhuseyin.com/blog/dev/create-thumbnails-imagefield-django/
# import io, re
import codecs
import os
import datetime
from datetime import timedelta

from django.core.files.storage import FileSystemStorage, Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import StringIO

from django.conf import settings
import pandas as pd
from projects import models as pro_models
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.contrib import messages
from pathlib import Path
from email.mime.image import MIMEImage
from django.utils.encoding import smart_str

import pandas as pd

images = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'images'))
thumbs = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'thumbnails'))


def import_actions(csv_file="/home/abdel/Documents/www/Book2.csv"):
    """
    import data from file csv
    """
    # encoding file "utf-8" or "ISO-8859-1"
    data =  pd.read_csv(csv_file,  encoding = "ISO-8859-1")
    """
    for elem in data.iterrows():
        tt = pro_models.Ticket(project_id=25, title=str(elem.capitalize()),  description=str(elem.capitalize()), author_id=3 ,  sequence=10, )
        tt.save()
    """

    queryset  = data.iteritems()
    for key, val in  queryset :
        # print val
        ind = ind + 1



def import_ticket(csv_file="/home/abdel/Documents/www/Book3.csv", project_pk=25):
    ligne = ""
    sequence = 10
    with codecs.open(csv_file, "r", "utf-8") as fd:
        while True:
         ligne = fd.readline()
         sequence = sequence + 10
         if ligne  :
             ligne = re.sub(r'"' , '', ligne)
             tt = pro_models.Ticket(project_id=project_pk,
                                    title=ligne[:250].capitalize(),
                                    description=ligne.capitalize(),
                                    author_id=3 ,
                                    category_id=3 ,
                                    sequence=10,
                                    )
             tt.save()
         else :
             break


IMAGE_MAX_SIZE = 1032150
THUMB_MAX_SIZE = 800

def create_thumbnail(infile, outfile, extension):
    """Returns the image resized to fit inside a box of the given size"""
    size = (128, 128)

    try:
        im = Image.open(infile)
        #im.thumbnail(size, Image.ANTIALIAS)
        im.thumbnail(size)
        im.save(outfile, "JPEG")
        """
        temp = StringIO()
        image.save(temp, extension)
        temp.seek(0)
        """
    except IOError:
        msg =  "cannot create thumbnail for", infile
        return False

    return True

    # return SimpleUploadedFile('temp', temp.read())

def save_thumbnail(document_file, document_fullname):
    # on va convertir l'image en jpg
    filename = document_fullname.splitext(path.split(document_fullname)[-1])[0]
    filename = "%s.jpg" % filename

    image = Image.open(document_file)

    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    # d'abord la photo elle-même
    create_thumbnail(image,  IMAGE_MAX_SIZE)

    # puis le thumbnail


def update_by_col():
    """
    """
    from django.db.models import F, Value

    # List all events of project
    tt.update(end_date = F('created'))
    return True



def omit_dates(df, list_years, list_dates, omit_days_near=3, omit_weekends=False):
    '''
    Comment exclude les jours de congés
    d'abord pip install holidays

    Given a Pandas dataframe with a DatetimeIndex, remove rows that have a date
    near a given list of dates and/or a date on a weekend.

    Parameters:
    ----------

    df : Pandas dataframe

    list_years : list of str
        Contains a list of years in string form
    list_dates : list of str
        Contains a list of dates in string form encoded as MM-DD
    omit_days_near : int
        Threshold of days away from list_dates to remove. For example, if
        omit_days_near=3, then omit all days that are 3 days away from
        any date in list_dates.
    omit_weekends : bool
        If true, omit dates that are on weekends.

    Returns:
    -------
    Pandas dataframe
        New resulting dataframe with dates omitted.
    '''

    if not isinstance(df, pd.core.frame.DataFrame):
        raise ValueError("df is expected to be a Pandas dataframe, not %s" % type(df).__name__)

    if not isinstance(df.index, pd.tseries.index.DatetimeIndex):
        raise ValueError("Dataframe is expected to have an index of DateTimeIndex, not %s" %
                         type(df.index).__name__)

    if not isinstance(list_years, list):
        list_years = [list_years]

    if not isinstance(list_dates, list):
        list_dates = [list_dates]

    result = df.copy()

    if omit_weekends:
        result = result.loc[result.index.dayofweek < 5]

    omit_dates = [ '%s-%s' % (year, date) for year in list_years for date in list_dates ]

    for date in omit_dates:
        result = result.loc[abs(result.index.date - datetime.strptime(date, '%Y-%m-%d').date()) > timedelta(omit_days_near)]


"""

exemple

import holidays
import pandas as pd
import numpy as np

years = ['2016', '2017']
holiday_dates = ['12-10', '12-25', '12-31', '01-01']
omit_dates(df, years, holiday_dates, omit_days_near=2, omit_weekends=True)

Extracting Holidays
If you open the documentation of Holidays library and scroll down a bit, you’ll see a list of 50-ish supported countries.
It’s now very easy to extract holidays, you’ll need to loop over the holidays in the country of interest, and also specify the year(s) of interest:

import holidays
import pandas as pd
import numpy as np

fr_vacances = []
aujourdhui = datetime.datetime.now()

for vacance in holidays.France(years=2019).items():
    print str(vacance[0])
    fr_vacances.append(str(vacance[0]))

# -- out
   ...:
(datetime.date(2020, 6, 1), 'Lundi de Pentecote')
(datetime.date(2020, 12, 25), 'NoEl')
(datetime.date(2020, 7, 14), 'Fete nationale')
(datetime.date(2020, 8, 15), 'Assomption')
(datetime.date(2020, 5, 21), 'Ascension')
(datetime.date(2020, 11, 11), 'Armistice 1918')
(datetime.date(2020, 4, 13), 'Lundi de Paques')
(datetime.date(2020, 5, 1), 'Fete du Travail')
(datetime.date(2020, 11, 1), 'Toussaint')
(datetime.date(2020, 1, 1), "Jour de l'an")
(datetime.date(2020, 5, 8), 'Armistice 1945')


aujourdhui = datetime.datetime.now()
jours_ouvrable = pd.bdate_range( aujourdhui.strftime("%Y-%m-%d") , "2020-05-31")
# les jour de vacance dans cette echantillons de jours_ouvrable
dd = [ 1 if str(val).split()[0] in fr_vacances else 0 for val in jours_ouvrable ]
#
pf = pd.DataFrame(data=jours_ouvrable)
pf['Is_Holiday'] = [1 if str(val).split()[0] in fr_vacances else 0 for val in jours_ouvrable ]

"""

from datetime import date
import holidays
import pandas as pd
import datetime


def get_jours_ouvrable(date1, date2):
    """
    pd.bdate_range( date_debut, date_fin ) permet de calculer
    les jours ovrable entre 2 dates
    input :: str : date1,
    input :: str : date2
    return :: retour pandas datatype liste de date vacances pour ces 2 ans
    """
    aujourdhui = datetime.datetime.now()
    date_debut  = str(date1)
    date_fin    = str(date2)
    return pd.bdate_range( date_debut, date_fin )

def get_jours_vacance(annees=[]):
    """
    input :: annee
    return :: retour la liste de date vacances pour cette annee
    """
    fr_vacances = []
    if len(annees) > 0 :
        for vacance in holidays.France(years=annees).items():
            fr_vacances.append(str(vacance[0]))
    return fr_vacances


def delai_due_date(self):
    aujourdhui = datetime.datetime.now()
    if self.due_date :
        # return  (aujourdhui - self.due_date ).days
        jours_ouvrable = len(pd.bdate_range( aujourdhui.strftime("%Y-%m-%d") , self.due_date.strftime("%Y-%m-%d") ))
        return -jours_ouvrable
    else :
        return False

def jours_ouvrable_exclude_vacances(date1, date2):
    """
    return : dataFrame qui reprente les jours ouvrables en excluant les jour de vacances française
    """
    aujourdhui = datetime.datetime.now()

    date_ouvrables = get_jours_ouvrable(date1, date2)
    # dd = [ 1 if str(val).split()[0] in fr_vacances else 0 for val in date_ouvrables ]
    #
    pf = pd.DataFrame(data=date_ouvrables, columns=['jours_ouvrable'])
    #
    # les jour de vacance dans cette echantillons de jours_ouvrable
    date_vacances = get_jours_vacance([int(date1), int(date2)])
    pf['holiday'] = pd.DataFrame(data=date_vacances)
    #
    # res = [str(elem[1]) for index, elem in  pf.items()]
    # res = [elem  for elem, index in  pf.values if index == 1]
    #
    list_jours_vacances   = [ elem for elem in  pf['holiday'].values if type(elem) == str ]
    list_jours_ouvrable   = [ elem.strftime('%Y-%m-%d') for elem in pf['jours_ouvrable']  ]
    #
    # pf['is_holiday'] = [1 if str(val).split()[0] in fr_vacances else 0 for val in date_ouvrables ]

    jours_ouvrable_exclude_vacances = [ elem for  elem in list_jours_ouvrable if elem not in list_jours_vacances]

    return jours_ouvrable_exclude_vacances


"""
us_holidays = holidays.UnitedStates()
# or:
# us_holidays = holidays.US()
# or:
# us_holidays = holidays.CountryHoliday('US')
# or, for specific prov / states:
# us_holidays = holidays.CountryHoliday('US', prov=None, state='CA')

date(2015, 1, 1) in us_holidays  # True
date(2015, 1, 2) in us_holidays  # False

# The Holiday class will also recognize strings of any format
# and int/float representing a Unix timestamp
'2014-01-01' in us_holidays  # True
'1/1/2014' in us_holidays    # True
1388597445 in us_holidays    # True

us_holidays.get('2014-01-01')  # "New Year's Day"

us_holidays['2014-01-01': '2014-01-03']  # [date(2014, 1, 1)]

us_pr_holidays = holidays.UnitedStates(state='PR')  # or holidays.US(...), or holidays.CountryHoliday('US', state='PR')

# some holidays are only present in parts of a country
'2018-01-06' in us_holidays     # False
'2018-01-06' in us_pr_holidays  # True

# Easily create custom Holiday objects with your own dates instead
# of using the pre-defined countries/states/provinces available
custom_holidays = holidays.HolidayBase()
# Append custom holiday dates by passing:
# 1) a dict with date/name key/value pairs,
custom_holidays.append({"2015-01-01": "New Year's Day"})
# 2) a list of dates (in any format: date, datetime, string, integer),
custom_holidays.append(['2015-07-01', '07/04/2015'])
# 3) a single date item
custom_holidays.append(date(2015, 12, 25))

date(2015, 1, 1) in custom_holidays  # True
date(2015, 1, 2) in custom_holidays  # False
'12/25/2015' in custom_holidays      # True

# For more complex logic like 4th Monday of January, you can inherit the
# HolidayBase class and define your own _populate(year) method. See below
# documentation for examples.

"""

def import_services(csv_file="/home/abdel/Documents/www/trw/liste_services.sql"):
    """
    """

    with codecs.open(csv_file, "r", "utf-8") as fd:
        while True:
            elem = fd.readline()

            if elem :
                service  = models.Service(name=elem.capitalize(), societe_id=2)
                try :
                    service.save()
                except Exception as err:
                    pass
            else:
                break


def export_as_json(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


def export_as_cvs(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
    writer = csv.writer(response)
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.code_of),
            smart_str(obj.client),
        ])
    return response



def api_test(request):
    queryset = models.DjangoOf.objects.filter(semaine=38, annee=18)
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


def liste_fichiers_fantome():
    #
    mes_doc = []
    projects = pro_models.objects.all()
    for pr in projects :
        docs = pr.get_documents_project()
        #
        for elem in docs :
            if os.path.exists(elem.document.document.path) :
                mes_doc.append(elem)

#-------------------
#-- Envoie d'email
#------------------
def send_html_email(subject, text_content, to_users, url_target , context=None):
    # send Email
    # FROM_ADMIN  = "informatique@strandcosmeticseurope.com"
    FROM_ADMIN  = "informatique@msbeautilab.com"
    # TO_USER = "asadquaoui@strandcosmeticseurope.com"

    # c = Context({'username': ticket.assignee.email })
    # text_content = render_to_string('mail/email.txt', c)
    # html_content = render_to_string('mail/email.html', c)
    #-------------------
    # Email alternative
    #-------------------

    context_plus = Context({'username': to_users[0],
                 'url_task': url_target,
                 })

    html_content = render_to_string('emails/email_alert_addtask.html' , context)
    #
    email = EmailMultiAlternatives(subject,
                                 html_content,
                                 FROM_ADMIN,
                                 to_users)
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    email.content_subtype = "html" # set the primary content to be text/html
    email.attach_alternative(html_content, "text/html")
    # email.attach('logo.png', "http://localhost:8000/static/images/logo/logo_strand_3D_001.png", 'image/png')

    # attache Image
    image_object = FileSystemStorage(location=os.path.join(settings.STATIC_ROOT, 'images', 'logo', 'logo_strand_3D_001.png'))
    #image_object = Storage( os.path.join(settings.STATIC_ROOT, 'images', 'logo', 'logo_strand_3D_001.png'))
    image_path =  os.path.join(settings.STATIC_ROOT, 'images', 'logo', 'logo_strand_3D_001.png')
    image_name = Path(image_path).name
    # email.attach('logo.png', image_path, 'image/png')

    # if os.path.exists(image_path) :
    with open(image_path, mode='rb') as f:
        image = MIMEImage(f.read())
        email.attach(image)
        image.add_header('Content-ID',  "<%s>".format(image_name))

    # email.attach_file('/images/weather_map.png')
    # email.mixed_subtype = 'related' # it is an important part that ensures embedding of an image
    email.send()
    # messages.success(request, _("Envoie email Your ticket has been registered. %s " % FROM_ADMIN))
    ## Sending notifications to a single user assigne
    message = u"Une tache ajoutée a votre espace de travail "
    return email


"""
Why not adding a middleware with something like this :
"""
import threading
from threading import Thread

class RequestMiddleware(object):

    thread_local = threading.local()

    def process_request(self, request):
        RequestMiddleware.thread_local.current_user = request.user

"""
 and later in your code (specially in a signal in that topic) :
"""

def signal_send_email():
    thread_local = RequestMiddleware.thread_local
    if hasattr(thread_local, 'current_user'):
        user = thread_local.current_user
    else:
        user = None

#---------------------------------------------
#--
#--------------------------------------------

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.request import HTTPError
    from urllib.request import URLError

except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib2 import URLError

import socket


URL_CHECK = 'http://localhost:80/server-status'
CMD_START = 'apache2ctl start'

def apache_running():
	"""Vérifie le statut d'Apache"""
	try:
		res = urlopen(URL_CHECK)
	except HTTPError:
		# réponse inattendue (URL_CHECK désactivé ?)
		# mais Apache répond
		return True
	except (socket.timeout, URLError):
		# pas de réponse ou erreur
		return False
	#
	return True


def check_apache():
    """ surveille l'état du daemon Apache """
    if not apache_running():
        # Tests sur le système
        # run_audit()
        # Apache doit être relancé
        call(CMD_START, shell=True)
        if apache_running():
            print('Apache relancé avec succès')
        else:
            print('Impossible de relancer Apache')
    else:
        print('État OK')


check_apache()
