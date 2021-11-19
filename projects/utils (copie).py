# -*- coding: utf-8 -*-
# Extension of http://www.yilmazhuseyin.com/blog/dev/create-thumbnails-imagefield-django/
# updated for Python 3

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from cStringIO import StringIO
import io, re
import codecs
import os
from django.conf import settings
import pandas as pd
from projects import models as pro_models
from core.profile import  models

images = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'images'))
thumbs = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'thumbnails'))

def import_actions(csv_file="/home/abdel/Documents/www/Book2.csv"):
    """
    import data from file csv
    ALTER TABLE `profile_societe` DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci;
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
        service  = models.Service(name=str(elem.capitalize()),  description=str(elem))
        service.save()
        ind = ind + 1

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



def api_test(request):
    queryset = models.DjangoOf.objects.filter(semaine=38, annee=18)
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response



def export_as_json(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

from django.utils.encoding import smart_str

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
