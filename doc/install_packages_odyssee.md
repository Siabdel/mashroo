## Install serveur APACHE2

> install apache2

```py
# aptitude install  apache2
$ fab  install_apache2  -f preparation_serveur.py
$ fab  install_module_image  -f preparation_serveur.py
```
###  install du module wsgi

```py
$ sudo apt-get install python-pip apache2 libapache2-mod-wsgi
$ sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3

```

## deployment sur serveur APACHE2


> For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/


###  Activer le module wsgi

```py
$ sudo a2enmode wsgi
$ sudo a2enmod suexec rewrite ssl actions include
$ sudo systemctl restart apache2
# si pb
$ sudo systemctl status apache2
$ sudo journalctl -xe
```

### Tester le module wsgi

```py
# version apache2
$ httpd -v
#
$ curl -I -L http://192.168.11.30:95
$ curl  -X GET http://192.168.11.30:95
# du cote envGterp
./manage.py check --deploy
```

## Mise en production sur APACHE2

### adduser django
```py

$ sudo adduser django
$ sudo adduser django  -G sudo

```


## install virtualenv && et install project gterprod

```py
pip install -U pip

$ fab make_virtualenv  -f preparation_local.py

$ mkvirtualenv envGterp
$ cdvirtualenv
$ tar xvfz ~/Documents/install/planning_19Mai20_v2.05.tar.gz
#
$ pip install -r requires_fev2020.txt
```


## install Driver ODBC Driver 17


```py
$ sudo curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
$ sudo ACCEPT_EULA=Y apt-get install msodbcsql17
$ sudo echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
$ sudo echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

##
$ sudo apt install odbcinst1debian2 libodbc unixodbc
$ sudo apt-get install unixodbc-dev
$ sudo apt-get install libgssapi-krb5-2
$ pip install django-pyodbc-azure==1.11.13.1

#

sudo ln -s x86_64-linux-gnu/libodbccr.so.2 libodbccr.so.1
$ sudo ln -s x86_64-linux-gnu/libodbcinst.so.2 libodbcinst.so.1
$ sudo ln -s libssl.so.0.9.8 libssl.so.10
$ sudo ln -s libcrypto.so.0.9.8 libcrypto.so.10

```


## creation des repertoire www

```c
cd /var/www/
mkdir django django/gterprod/ django/gterprod/static
sudo chmod 755 -R django/
sudo chown django:django -R django
#
# copie des fichiers static
$ sudo cp -R /home/django/.virtualenvs/envGterp/planning/project/static/*   /var//www/django/gterprod/static/
$ sudo cp -R /home/django/.virtualenvs/envGterp/planning/ofschedule/static/*   /var//www/django/gterprod/static/
$ sudo cp -R /home/django/.virtualenvs/envGterp/planning/approvisionnement/static/*   /var//www/django/gterprod/static/
```
## Creation du fichier wsgi.py

```py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
sys.path.append('/home/django/.virtualenvs/envGterp/lib/python2.7/site-packages')
sys.path.append('/home/django/.virtualenvs/envGterp/planning')
sys.path.append('/home/django/.virtualenvs/envGterp/planning/planning')

os.environ['DJANGO_SETTINGS_MODULE'] = "planning.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planning.settings")

from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
    print("WSGI without exception")

except Exception:
    print("Abdel handling WSGI exceptioni !!!!")
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
```
## Configuration du virtualhost apache


```html
$ sudo more  /etc/apache2/sites-available/gterprod.conf
#

WSGIDaemonProcess www.gterprod python-path=/home/django/.virtualenvs/envGterp/planning:/home/django/.virtualenvs/envGterp/lib/python2.7/site-packages
  WSGIProcessGroup www.gterprod
  WSGIScriptAlias / /home/django/.virtualenvs/envGterp/planning/planning/wsgi.py

<VirtualHost *:90>
 ServerAdmin contacte@msbeautilab.com
 ServerName www.gterprod
 ServerAlias www.www.gterprod
 ErrorLog /var/log/apache2/error.log

   Alias /favicon.ico /var/www/django/gterprod/static/favicon.ico
   Alias /static/ /var/www/django/gterprod/static/
   Alias /media/ /var/www/django/gterprod/media/

<Directory /var/www/django/gterprod/apache/>
  # Require all granted # si apache2 ver > 2.4
  Order deny,allow
  Allow from all
</Directory>

<Directory /var/www/django/gterprod/static/>
  # Require all granted # si apache2 ver > 2.4
  Order deny,allow
  Allow from all
</Directory>

<Directory /var/www/django/gterprod/media/>
  # Require all granted # si apache2 ver > 2.4
  Order deny,allow
  Allow from all
</Directory>



```



## Divers :

```py
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
$ pip install cffi==1.5.2
```

### si erreur au lancement http://192.168.11.30/admin
```py
importError at /admin/
cannot import name properties

```

> il faut ajouter les lignes dans gterprod.conf.



```py
WSGIDaemonProcess www.gterprod python-path=/home/django/.virtualenvs/envGterp/planning:/home/django/.virtualenvs/envGterp/lib/python2.7/site-packages
WSGIProcessGroup www.gterprod
```

### VM Odyssee install packages

| Name | Desc | Fait ok |  |
| --- | --- | --- | --- |
|auth==0.5.3| package authentification securisé| ok |
|backports.functools-lru-cache==1.5| | ok |
|backports.shutil-get-terminal-size==1.0.0| cache: backport of functools.lru_cach | ok |
|blinker==1.4| The library lets signalers send messages to connected receiver function| ok |
|cairocffi==0.9.0| Python module providing bindings for the cairo graphics library| ok |
|CairoSVG==1.0.22|Python module providing bindings for the cairo graphics library | ok |
|certifi==2018.4.16| pip install python-certifi  linux, win32. | ok |
|cffi==1.12.3| | ok |
|chardet==3.0.4| The Universal Character Encoding Detector| ok |
|convertdate==2.2.1| The convertdate package was originally developed a| ok |
|cssselect2==0.2.1| cssselect2 is a straightforward implementation of CSS3 Selectors for markup documents | ok |
|cycler==0.10.0| Create a new Cycler object from a single positional argument, a pair of positional arguments, or the combination of keyword arguments.| ok |
|decorator==4.3.0| | ok |
|Django==1.11.16| | ok |
|django-allauth==0.38.0| | ok |
|django-annoying==0.10.4| | ok |
|django-appconf==1.0.3| | ok |
|django-avatar==4.1.0| | ok |
|django-bower==5.2.0| | ok |
|django-debug-toolbar==1.9.1| | ok |
|django-easy-pdf==0.1.1| | ok |
|django-jsonfield==1.3.1| | ok |
|django-model-utils==3.2.0| | ok |
|django-mssql==1.8| | ok |
|django-notifications-hq==1.5.0| | ok |
|django-notify-x==0.1.9| | ok |
|django-pandas==0.5.1| | ok |
|django-pyodbc==1.1.3| | ok |
|django-pyodbc-azure==1.11.13.1| | ok |
|django-queryset-csv==1.0.1| | ok |
|django-rest-framework==0.1.0| | ok |
|django-scheduler==0.7.5| | ok |
|django-taggit==0.24.0| | ok |
|djangorestframework==3.9.4| | ok |
|dnspython==1.16.0| | ok |
|enum34==1.1.6| | ok |
|eventlet==0.25.1| | ok |
|falcon==2.0.0| | ok |
|functools32==3.2.3.post2| | ok |
|future==0.16.0| | ok |
|greenlet==0.4.15| | ok |
|gunicorn==19.10.0| | ok |
|holidays==0.10.2| | ok |
|html5lib==1.0.1| | ok |
|icalendar==4.0.2| | ok |
|idna==2.7| | ok |
|ipython==5.8.0| | ok |
|ipython-genutils==0.2.0| | ok |
|jsonfield==2.0.2| | ok |
|jsonschema==2.6.0| | ok |
|jupyter-core==4.4.0| | ok |
|kiwisolver==1.0.1| | ok |
|korean-lunar-calendar==0.2.1| | ok |
|matplotlib==2.2.3| | ok |
|mongoengine==0.18.2| | ok |
|monotonic==1.5| | ok |
|nbformat==4.4.0| | ok |
|numpy==1.15.4| | ok |
|oauthlib==2.1.0| | ok |
|opencv-python==3.4.5.20| | ok |
|panda==0.3.1| | ok |
|pandas==0.23.4| | ok |
|pathlib2==2.3.2| | ok |
|pbr==5.1.3| | ok |
|pdfkit==0.6.1| | ok |
|pdfrw==0.4| | ok |
|pexpect==4.6.0| | ok |
|pickleshare==0.7.4| | ok |
|Pillow==6.0.0| | ok |
|pkg-resources==0.0.0| | ok |
|plotly==3.4.2| | ok |
|prompt-toolkit==1.0.15| | ok |
|ptyprocess==0.6.0| | ok |
|pycparser==2.19| | ok |
|Pygments==2.2.0| | ok |
|PyMeeus==0.3.7| | ok |
|pymongo==3.9.0| | ok |
|pyodbc==4.0.23| | ok |
|pyparsing==2.3.0| | ok |
|PyPDF2==1.26.0| | ok |
|Pyphen==0.9.5| | ok |
|python-dateutil==2.7.5| | ok |
|python-openid==2.2.5| | ok |
|pytz==2018.7| | ok |
|reportlab==3.5.23| | ok |
|requests==2.19.1| | ok |
|requests-oauthlib==1.0.0| | ok |
|retrying==1.3.3| | ok |
|scandir==1.9.0| | ok |
|scipy==1.2.1| | ok |
|simplegeneric==0.8.1| | ok |
|six==1.15.0| | ok |
|sqlparse==0.2.4| | ok |
|stevedore==1.30.1| | ok |
|subprocess32==3.5.3| | ok |
|tinycss2==0.6.1| | ok |
|traitlets==4.3.2| | ok |
|unicodecsv==0.14.1| | ok |
|Unidecode==1.0.22| | ok |
|urllib3==1.23| | ok |
|virtualenv==16.7.3| | ok |
|wcwidth==0.1.7| | ok |
|WeasyPrint==0.42.3| | ok |
|webencodings==0.5.1| | ok |
|Werkzeug==0.16.0| | ok |
|xhtml2pdf==0.2.3| | ok |
|yamlog==0.9| | ok |
|zebra==0.0.5| | ok |
|| | ok |
