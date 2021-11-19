# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
# Data analysis
import os, sys
import datetime
import pytz
import json
import pylab
import io
import base64
import matplotlib
import csv
import random
from dateutil.rrule import advance_iterator, rrule, DAILY
# pandas
from io import StringIO
from django.utils.encoding import smart_str
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas, FigureCanvasAgg
import numpy as np
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
from django_pandas.io import read_frame
import pandas as pd

 # from dateutil.parser import *
from django.shortcuts import  redirect as  redirect_to, render, reverse, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse
from django.utils import timezone
from django.core import serializers
from django.views.generic.edit import UpdateView, CreateView, DeleteView, ModelFormMixin, ProcessFormView, FormView, FormMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import messages
# local
from mashroo.settings import PROJECT_PATH
from mashroo import settings

import businessce.models as planmodels
import unidecode  # pour finir avec les chaine accentué
# pdf file
import pdfkit as pdf_kit
from django.template.loader import get_template
from django.template import Context
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from businessce.utils import all_columns_class, all_records_panda
from core.profile import views as profilviews
from core.profile import models as profil_model

def simple_pandas_matplotlib__(request):

    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    # OF
    #ofs = planmodels.DjangoOf.objects.filter(statut = 'C').values('machine_travail').distinct().order_by('-semaine')
    ofs = planmodels.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=[
                    'semaine', 'machine_travail_id', 'quantite_prevue'])
    # total des quantite prevue par semaine
    df.groupby('semaine').quantite_prevue.sum()
    # total des quantite prevue par semaine et machine
    df.groupby(['machine_travail_id', 'semaine']).quantite_prevue.sum()

    # df.head(5)
    df[:30].plot()
    x = 0
    h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='Green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    response = HttpResponse(df.plot(), content_type='image/png')
    return response


def simple_test_matplotlib(request):
    import matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    from mashroo.settings import PROJECT_PATH
    from django_pandas.io import read_frame
    import pandas as pd
    import matplotlib
    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    # OF
    ofs = planmodels.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id__nommach', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=['semaine', 'machine_travail_id', 'quantite_prevue'])

    #x = np.arange(10)
    x = h = []
    for elem in ofs:
        machine, machine, quantite_prevue = elem
        x.append(machine[:1])
        h.append(str(float(quantite_prevue) / 100))

    #h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine semaine 37')
    #plt.xlim(0, 10)
    #plt.ylim(0, 8)
    plt.xlabel('Machines')
    plt.ylabel('quantite prevue')
    bar1 = plt.bar(x, h,
                   width=0.5,
                   bottom=0,
                   color='Blue',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    with open(os.path.join(base_dir_media, "testPlot.png"), "wb") as fd:
        fd.write(buf.getvalue())

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


def mplimage1(request):
    # 1-
    # matplotlib.use('Agg')
    ofs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])
    plt.legend()

    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)
    matplotlib.pyplot.close(fig)
    buffer = cStringIO.StringIO()
    cropped_img.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    return HttpResponse(img_str, content_type='image/png')

#@api.multi


def mplimage2(request, kind):

    # 1-
    # matplotlib.use('Agg')
    ofs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])

    if kind == "1":
        df.plot(kind="line", stacked=True)
    elif kind == 2:
        df.plot(kind="bar", stacked=True)
    elif kind == "3":
        df.plot(kind="barh", stacked=True)
    elif kind == "4":
        df.plot(kind="kde", stacked=True)
    elif kind == "5":
        df.plot(kind="density", stacked=True)
    elif kind == "6":
        df.plot(kind="area", stacked=True)
    else:
        df.plot(kind="bar", stacked=True)

    # 2 --
    dfg = df.groupby('machine_travail')
    rs = dfg.sum(level='machine_travail')

    x = list(rs.axes[0])
    columns = list(df.columns)
    h = [2900.0, 5000.0,    3000.0,  5000.0, 10083.0, 13500.0,
         4470.0, 10083.0,  2500.0,  5500.0,  8321.0, 12000.0]
    #h = x
    plt.title(columns)
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('Machine Conditionnment')
    plt.ylabel('Quantite commandee')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    matplotlib.pyplot.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    # if required clear the figure for reuse
    # Register a function to be run once
    fig.clear()
    return response
#----------------------
# MATPLOTLIB
#--------------------
def simple_pandas_matplotlib(request):
    #
    response = HttpResponse("ok...", content_type='image/png')
    return response


def simple_pandas_matplotlib__(request):
    import matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    from mashroo.settings import PROJECT_PATH
    from django_pandas.io import read_frame
    import pandas as pd
    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    # OF
    #ofs = planmodels.DjangoOf.objects.filter(statut = 'C').values('machine_travail').distinct().order_by('-semaine')
    ofs = planmodels.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=[
                    'semaine', 'machine_travail_id', 'quantite_prevue'])
    # total des quantite prevue par semaine
    df.groupby('semaine').quantite_prevue.sum()
    # total des quantite prevue par semaine et machine
    df.groupby(['machine_travail_id', 'semaine']).quantite_prevue.sum()

    # df.head(5)
    df[:30].plot()
    x = 0
    h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='Green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    response = HttpResponse(df.plot(), content_type='image/png')
    return response


def simple_test_matplotlib(request):
    import matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    from mashroo.settings import PROJECT_PATH
    from django_pandas.io import read_frame
    import pandas as pd
    import matplotlib
    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    # OF
    ofs = planmodels.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id__nommach', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=[
                    'semaine', 'machine_travail_id', 'quantite_prevue'])

    #x = np.arange(10)
    x = h = []
    for elem in ofs:
        machine, machine, quantite_prevue = elem
        x.append(machine[:1])
        h.append(str(float(quantite_prevue) / 100))

    #h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine semaine 37')
    #plt.xlim(0, 10)
    #plt.ylim(0, 8)
    plt.xlabel('Machines')
    plt.ylabel('quantite prevue')
    bar1 = plt.bar(x, h,
                   width=0.5,
                   bottom=0,
                   color='Blue',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    with open(os.path.join(base_dir_media, "testPlot.png"), "wb") as fd:
        fd.write(buf.getvalue())

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


def mplimage1(request):

    # 1-
    # matplotlib.use('Agg')
    ofs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])
    plt.legend()
    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)
    matplotlib.pyplot.close(fig)
    buffer = cStringIO.StringIO()
    cropped_img.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    return HttpResponse(img_str, content_type='image/png')

#@api.multi


def mplimage2(request, kind):

    # 1-
    # matplotlib.use('Agg')
    ofs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])

    if kind == "1":
        df.plot(kind="line", stacked=True)
    elif kind == 2:
        df.plot(kind="bar", stacked=True)
    elif kind == "3":
        df.plot(kind="barh", stacked=True)
    elif kind == "4":
        df.plot(kind="kde", stacked=True)
    elif kind == "5":
        df.plot(kind="density", stacked=True)
    elif kind == "6":
        df.plot(kind="area", stacked=True)
    else:
        df.plot(kind="bar", stacked=True)

    # 2 --
    dfg = df.groupby('machine_travail')
    rs = dfg.sum(level='machine_travail')

    x = list(rs.axes[0])
    columns = list(df.columns)
    h = [2900.0, 5000.0,    3000.0,  5000.0, 10083.0, 13500.0,
         4470.0, 10083.0,  2500.0,  5500.0,  8321.0, 12000.0]
    #h = x
    plt.title(columns)
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('Machine Conditionnment')
    plt.ylabel('Quantite commandee')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    matplotlib.pyplot.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    # if required clear the figure for reuse
    # Register a function to be run once
    fig.clear()
    return response


def construct_columns(mes_columns):
    """
    construit un tableau columns pour bootstrap_table
    """
    all_columns = [smart_str(elem) for elem in mes_columns]
    columns = [{smart_str('field'):  elem, smart_str('title'): elem , smart_str('type'): smart_str('datetime')}
                    for elem  in all_columns
            ]
    # column = dict(zip(all_columns, row))
    return columns

#---------------------------
#--- Panda of view
#---------------------------
def PandasOfView(request):
  template = 'pandas_of.html'

  qs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18').values_list(
      'code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
  #df = qs.to_dataframe()
  df = read_frame(qs, fieldnames=['machine_travail', 'quantite_commandee'])
  dfg = df.groupby(df['machine_travail']).sum()

  # trier par quantitee
  dfg.sort_values('quantite_commandee')
  indexes = list(dfg.axes[0])

  data = [{'field':  index, 'title': elem} for index, elem in dfg]
  columns = construct_columns(df.columns)

  #Format the column headers for the Bootstrap table, they're just a list of field names,
  #duplicated and turned into dicts like this: {'field': 'foo', 'title: 'foo'}
  #columns = [{'field': champ, 'title': champ} for champ in DjangoOf._meta.get_fields()]

  #Write the DataFrame to JSON (as easy as can be)
  # output just the records (no fieldnames) as a collection of tuples
  json = dfg.to_json(orient='records')
  #Proceed to create your context object containing the columns and the data
  context = {
             'data': json,
             'columns': columns
            }
  #And render it!
  return render(request, template, context)


def query_of(request):
    """
    console de requete of
    """
    template = "console/of_crud.html"
    #And render it!
    context = dict()

    #qs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18' ).values_list('code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
    qs = planmodels.DjangoOf.objects.filter(annee='18').order_by(
        '-date_debut_reelle')  # Use the Pandas Manager
    #df = read_frame(qs, fieldnames = ['machine_travail', 'quantite_commandee'])
    df = read_frame(qs,
                    fieldnames=['id', 'code_of', 'statut', 'date_debut_reelle', 'semaine', 'annee',
                                'commande_id', 'machine_travail', 'client_id', 'quantite_prevue', 'quantite_commandee',
                                'quantite_realisee'])
    # entete de colonnes
    columns = construct_columns(df.columns)
    #Write the DataFrame to JSON (as easy as can be)
    #json = dfg.to_json(orient='records')  # output just the records (no fieldnames) as a collection of tuples
    # output just the records (no fieldnames) as a collection of tuples
    json = df.to_json(orient='records')
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': json,
             'columns': columns
            }
    return render(request, template, context)


def query_logging(request):
    """
    console de requete log
    """
    template = "console/of_crud.html"
    #And render it!
    context = dict()

    #qs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18' ).values_list('code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
    qs = planmodels.DjangoLogging.objects.all().order_by('-id')  # Use the Pandas Manager
    #df = read_frame(qs, fieldnames = ['machine_travail', 'quantite_commandee'])
    columns = [f.name for f in planmodels.DjangoLogging._meta.get_fields()]

    df = read_frame(qs, fieldnames=[
                    'id', 'code_erreur', 'programme_name', 'statut', 'description', 'created', 'created_by'])
    # entete de colonnes
    columns = construct_columns(df.columns)
    #Write the DataFrame to JSON (as easy as can be)
    #json = dfg.to_json(orient='records')  # output just the records (no fieldnames) as a collection of tuples
    # output just the records (no fieldnames) as a collection of tuples
    json = df.to_json(orient='records')
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': json,
             'columns': columns
            }
    return render(request, template, context)


def dictfetchall(sql):
    "Return all rows from a cursor as a dict"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        all_columns = [str(col[0]) for col in cursor.description]
        #
        data = [dict(zip(all_columns, row)) for row in cursor.fetchall()]
        # on traite les date
        data_clean = []
        for row in data:
            for columns, elem in row.items():
                if (type(elem) == datetime.date or type(elem) == datetime.datetime) and elem != None:
                                row[columns] = elem.isoformat()
            # recharge  data new
            data_clean.append(row)

        return all_columns, data_clean


def my_custom_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows

def plot_of_test(request):

    # ex donne en 4 :   df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
    # df2.plot.bar()

    # 1-
    fig = matplotlib.figure.Figure()
    canvas = FigureCanvasAgg(fig)

    # 2- canvas
    #buf = io.BytesIO()
    #canvas.print_png(buf)

    ofs = planmodels.DjangoOf.objects.filter(semaine='38', annee='18')

    # df = pd.DataFrame(ofs, columns = ['code_of', 'quantite_commandee'] )
    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_prevue'])
    #df.plot(ax=ax)
    df.plot(kind="bar", stacked=True)
    #plt.show()

    base_dir_media = PROJECT_PATH + '/media/'

    """
    with open(os.path.join(base_dir_media, "testPlot.png"), "wb") as fd_image :
        fd_image.write(buf.getvalue())
        #

        with open(os.path.join(base_dir_media, "testPlot.png"), "rb") as fd :
            response = HttpResponse(fd, content_type = 'image/png')
            #pylab.savefig(response, format="png")
    """

    output = StringIO.StringIO()
    fig.savefig(output, format="png")
    contents = output.getvalue()

    #
    plt.close(fig)
    response = HttpResponse(contents, content_type='image/png')
    #canvas.print_png(response)

    # 3 print
    #df.plot(kind="bar", stacked=True)
    #canvas.print_png(response)
    # plot  df.plot(kind='bar')
    # df.plot.hist(alpha=0.5)

    # hitogramme des ofs
    #plt.axhline(0, color='k')
    #plt.show()
    return response



#@method_decorator(login_required, 'dispatch')
#@permission_required('ofschedule.change_djangoof')
def dba_query(request, requete):
    """
    console de requete constraints name
    """
    template = "console/of_crud.html"
    #And render it!
    context = dict()

    # sql = " SELECT * FROM sys.objects "
    # df = planmodels.DjangoOf.objects.filter(semaine='38', annee='18' ).values_list('code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
    #rows = DjangoLogging.objects.raw("select * from categorie_transmission")   # Use the Pandas Manager
    if requete == '1':  # liste des foreighkey
        sql1 = "EXEC sp_fkeys 'transmission'"
        sql = "SELECT OBJECT_NAME(object_id) AS ConstraintName, SCHEMA_NAME(schema_id) AS SchemaName, type_desc AS ConstraintType FROM sys.objects WHERE SCHEMA_NAME(schema_id)='dbo'"
        sql3 = "SELECT OBJECT_NAME(object_id) AS ConstraintName, SCHEMA_NAME(schema_id) AS SchemaName, OBJECT_NAME(parent_object_id) AS TableName, type_desc AS ConstraintType FROM sys.objects WHERE type_desc LIKE '%CONSTRAINT%'"

    elif requete == '2':  # ligne de PDC
        sql = """
        SELECT TOP(10000)  * FROM tmpcharc
        WHERE ancond > '17'
        ORDER BY id DESC
        """

    elif requete == '3':  # Fiche de travail
        sql = """
        SELECT TOP(10000)  codefcndt, code_of, datecndt, codeartc, codecndt, cdesce, nbreacndt,
        nbrecndt, qteacndt, qtecndt, qtestock, datedcndt
        FROM ficwcndt
        WHERE cdesce IS NOT NULL and datecndt IS NOT NULL
        ORDER BY codefcndt DESC
        """

    elif requete == '4':
        sql = "SELECT TOP(1000) * FROM  ligappro ORDER BY cdeappro DESC,  lignappr  DESC"

    elif requete == '5':
        sql = """
        SELECT TOP(10000) * FROM  cde_clie
        WHERE ancond > '17'
        ORDER BY datepcnd DESC
        """

    elif requete == '6':  # doublons OFs
        sql = """
        SELECT * FROM ordre_fabrication WHERE code_of IN (
            SELECT  code_of
            FROM ordre_fabrication
            WHERE code_of is not null
            GROUP BY  code_of
            HAVING count(code_of) > 1
            )
        ORDER BY count(code_of) DESC
        """
    elif requete == '7':  # doublons OFs
        sql = """
            SELECT * FROM tmpcharc WHERE cdsce IN (
            SELECT cdesce, count(code_of) as nb
            FROM tmpcharc
            WHERE code_of is not null
            GROUP BY  cdesce,  code_of
             HAVING count(code_of) > 1
             )
             ORDER BY count(code_of) DESC
             """
    elif requete == '8':  # doublons OFs
        sql = """
            SELECT * FROM ordre_fabrication WHERE code_of NOT IN(
                SELECT  code_of
                FROM tmpcharc
                WHERE code_of is not null
             )
             ORDER BY count(code_of) DESC
             """
    elif requete == '9':  # Liste des view
        sql = """
            select O.name as [Object_Name], C.text as [Object_Definition]
            from sys.syscomments C
            inner join sys.all_objects O ON C.id = O.object_id
            --where C.text like '%table_name%'
            """
    elif requete == '10':  # liste des coloumns
        sql = "EXEC sp_columns 'ordre_fabrication'"
    else:
        sql = " SELECT TOP(100) * FROM sys.objects "

    # execute curseur
    all_columns, rows = dictfetchall(sql)
    #

    columns = ['id', 'created', 'libelle', 'description']
    # output just the records (no fieldnames) as a collection of tuples
    json_data = json.dumps(rows)
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': json_data,
             'columns': construct_columns(all_columns)

            }
    return render(request, template, context)


#@method_decorator(login_required, 'dispatch')
@permission_required('ofschedule.change_djangoof', login_url="/admin/login/")
def console_admin(request):
    """
    console admin base sur un composant du framework bootstrap = "bootstrap_table"
    jquery
    """
    template = "console/console_admin.html"
    #And render it!
    context = dict()
    return render(request, template, context)


from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin


class EasyPDFView(PDFTemplateResponseMixin, ListView):
    model = planmodels.DjangoOf
    queryset = planmodels.DjangoOf.objects.filter(semaine="28", annee="19")
    template_name = 'easy_pdf/test_pdf.html'


class JsonResponseMixin(object):
    """
    Return json
    """
    def render_to_json(self, queryset):
        # queryset  serialise
        data = serializers.serialize('json', queryset)
        json_data = json.loads( data)
        # json_data = json.dumps( data)
        data_light = [ (elem['pk'], elem['fields']) for elem in json_data ]
        data_light = [ ]
        for elem in json_data:
            elem['fields']['pk'] = elem['pk']
            data_light.append(elem['fields'])

        data_fin = json.dumps(data_light)
        return HttpResponse(data_fin ,  content_type='application/json')

    def queryset_to_json(self, queryset):
        # queryset  serialise
        data = serializers.serialize('json', queryset)

        json_data = json.loads( data)
        # json_data = json.dumps( data)

        # data_light = [ (elem['pk'], elem['fields']) for elem in json_data ]
        data_light = [ ]
        for elem in json_data:
            elem['fields']['pk'] = elem['pk']
            data_light.append(elem['fields'])

        return json.dumps(data_light)

    def dict_to_json(self, data):
        # queryset  serialise
        js_data = json.dumps( data)
        json_data = json.loads(js_data)
        data_light = [ elem  for elem in json_data ]
        return json.dumps(data_light)

    def export_as_json(self,  queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json",  queryset, stream=response)
        return response

    def export_as_cvs(self, queryset):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export_da_{}.csv'.format(queryset.first().pk)
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
        writer = csv.writer(response)
        # les colonnes
        nom_class = queryset.first().__class__
        # ecrire entete du fichier avec les libelles
        all_columns =  all_columns_panda(queryset)
        # writer.writerow(all_columns)

        # Ecrire les valeurs du queryset
        ind = 0
        data_dict = all_records_panda(queryset, fields=all_columns)
        # messages.add_message(self.request, messages.INFO, 'elem *** = %s' % data_dict)
        # --
        for ligne in data_dict:
            # Write to file
            if ligne and ind == 0:
                writer.writerow(ligne.keys())
            elif ligne :
                # write value
                writer.writerow(ligne.values())
            ind = ind + 1
        return response


    def export_as_pdf(self, queryset, fields=None):
        #------------------
        #-- panda to pdf
        #-----------------

        """
        df.to_html('test.html')
        PdfFilename='pdfPrintOut.pdf'
        pdf_kit.from_file('test.html', PdfFilename)
        """
        # les options de la mise en page
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
        # contruire le template
        template = get_template('console/test_pdf.html')
        # context
        df = read_frame(queryset, fieldnames= ["id", "code_of", "semaine", "created_by"])
        data = df.to_dict()
        context = Context({"data": data})  # data is the context data that is sent to the html file to render the output.
        html = template.render({"object_list": queryset})
        # from string html
        static_css = os.path.join(settings.STATIC_ROOT, 'css', 'bootstrap.css')
        pdf = pdf_kit.from_string(html, False,  options=options, css=static_css)
        # from url
        response = HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response



    def html_to_pdf_weasyprint(self, queryset):
        # contruire le template
        template = get_template('console/test_pdf.html')
        html_string = template.render({"object_list": queryset})

        html = HTML(string=html_string)
        css = CSS(string='@page { size: A4; margin: 1cm }')
        font_config = FontConfiguration()
        html.write_pdf(target='mypdf.pdf',  font_config=font_config);

        filename = os.path.join(settings.MEDIA_ROOT, 'mypdf.pdf')
        with  open(filename, "w") as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + filename
            return response

        return response


    def export_as_pdf_from_url(self, url_src, queryset, fields=None):
        """
        """
        # les options de la mise en page
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
        # context
        context = Context({"data": queryset})  # data is the context data that is sent to the html file to render the output.
        # from url

        pdf_out = os.path.join(settings.MEDIA_ROOT, 'outpdf.pdf')
        pdf = pdf_kit.from_url(url_src, pdf_out,  options=options)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response
# -----------------------------------------
# --- Gestion des Demande approv. confirmees
# -----------------------------------------
from businessce import forms
@method_decorator(login_required, 'dispatch')
class BusinessHomeView(  FormView, JsonResponseMixin):
    """
    Gestion console admin
    """
    template_name = "console/of_crud.html"
    form_class = forms.SearchForm

    def __init__(self,  **kwargs):
        """
        contructeur
        """
        super(BusinessHomeView, self).__init__(**kwargs)

    def get_context_data(self,  **kwargs):
        context = super(BusinessHomeView, self).get_context_data(**kwargs)
        # init panier Cart
        return context

    def get(self, request,  **kwargs):
        # 1- charger object_list d'abord
        #self.get_queryset(**kwargs)
        action= kwargs.get('action')

        # 2- charger context
        context = self.get_context_data(**kwargs)

        if action == 'listfk':
            sql4 = """
                SELECT OBJECT_NAME(parent_object_id) as table_name, OBJECT_NAME(object_id) AS ConstraintName,
                    SCHEMA_NAME(schema_id) AS SchemaName,
                    type_desc AS ConstraintType
                FROM sys.objects
                WHERE type_desc LIKE '%CONSTRAINT'
                --AND OBJECT_NAME(parent_object_id) like '%%'
                """

            # execute curseur
            all_columns, rows = dictfetchall(sql4)

            #
            # output just the records (no fieldnames) as a collection of tuples
            # Proceed to create your context object containing the columns and the data

            data_json =  self.dict_to_json(rows)
            context = {
                     'data': data_json,
                     'columns': construct_columns(all_columns)
                    }
            #
            return render(request, self.template_name, context)

        elif action == 'printpdf':
            # 4- creation Entete DA gestform
            queryset = planmodels.DjangoOf.objects.filter(semaine='28')
            return self.export_as_pdf(queryset)

        elif action == 'printpdf2':
            # 4- creation Entete DA gestform
            from utils import html_to_pdf
            queryset = planmodels.DjangoOf.objects.filter(semaine='28')
            return html_to_pdf(self.request, queryset)


        elif action == 'export':
            # 4- creation export Excel
            # export csv
            queryset = planmodels.DjangoOf.objects.filter(semaine='28')
            return self.export_as_cvs(queryset)

        elif action == 'pdfromurl':
            # 4- creation export Excel
            # export csv
            # queryset =  appmodels.Item.objects.all()
            return self.export_as_pdf_from_url("http://localhost:8000/da/printcart/", queryset)


        # retour
        return self.render_to_response(context)



def print_items_cart(request):
    # export csv
    # les options de la mise en page
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    # context
    # from url
    filename_pdf = os.path.join(settings.MEDIA_ROOT, 'mypdf.pdf')
    pdf = pdf_kit.from_url("http://localhost:8000/da/printcart/", filename_pdf , options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename=%s' % filename_pdf
    return response


def test_plot():
    import numpy as nb

    # %matplotlib inline
    # plt.__file__
    plt.figure()
    # 1er figure
    plt.subplot(2,2, 1)
    plt.plot(np.random.randn(100))
    # 2ieme figure
    plt.subplot(2,2, 2)
    plt.plot(np.random.random(size=100), "r+")
    # 3ieme figure
    plt.subplot(2,2, 3)
    plt.plot(np.random.randn(100), "r.")
    # 4iemefigure
    plt.subplot(2,2, 4)
    plt.plot(np.random.randn(100), "g--")
    plt.title("Evolution des temperature du globe 2019")
    #--
    plt.savefig("plt_temperature_2019.jpg")
    plt.show()


def test_plot2():
    import numpy as nb

    # %matplotlib inline
    # plt.__file__
    figure2 = plt.figure()
    # 1er figure
    # plt.subplot(2,2, 1)
    #--
    qs = planmodels.DjangoOf.objects.filter(semaine__gt=20).values_list(
        'semaine', 'commande_id', 'quantite_prevue').distinct()
    df = read_frame(qs, fieldnames=['semaine', 'quantite_prevue'])
    dfg = df.groupby('semaine').sum()
    dfg.aggregate('quantite_prevue')
    #-
    dfg.plot()
    # df.plot(ax=ax)
    # df.plot(kind="bar", stacked=True)
    # plt.plot(cmde_par_mois, "r+")
    #affichage
    plt.title("Evolution des commandes en 2019")
    #--
    plt.savefig("plt_commande_2019.jpg")

    # aa.show()
    return figure2


def tree_societes(request):
     #
     societes =  profil_model.Societe.objects.filter(pk=2).order_by('name')
     # render

     return render(request, "businessce/societes_list.html" , locals())
