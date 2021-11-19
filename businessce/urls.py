#-*- coding:utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.views.generic.list import ListView
from schedule.models import Calendar
from schedule.feeds import UpcomingEventsFeed
from schedule.feeds import CalendarICalendar
from schedule.periods import Year, Month, Week, Day
from schedule import views
from schedule.views import CreateCalendarView, ajax_list_calendar, FullCalendarView,\
CreateCalendarView, CreateEventView, CreateOccurrenceView, CreateEventViewRDV, UpdateCalendarView

from schedule.views import UpdateEventViewRDV
from ofschedule.views import FullCalendarView, api_get_ofs, api_move_of, api_update_qte_of, api_edit_of, api_get_machines, FullCalendarResourceView, FullCalendarEquipeView
from ofschedule.datanalysis import simple_test_matplotlib, simple_pandas_matplotlib
from django.conf.urls.static import static
from ofschedule import models
from ofschedule import utils
from businessce import views as biviews
#from ofschedule import datanalysis as biviews



urlpatterns = [

    # ---------------------
    # Django console Admin
    # ---------------------

    url(r'^admin/home', biviews.console_admin, name='console_admin'),
    url(r'^admin/ofcrud/', biviews.query_of, name='of_crud'),
    url(r'^admin/logging/', biviews.query_logging, name='of_logging'),
    url(r'^admin/dba_query/(?P<requete>[\d]{1,2})/$', biviews.dba_query, name='dba_query'),
    url(r'^console/(?P<action>[\w]+)/$', biviews.BusinessHomeView.as_view(), name='test_test'),
    url(r'^printpdf/', biviews.EasyPDFView.as_view(), name='print_pdf_test'),
    # PRINT PDF
    # http://localhost:8000/da/cart/listitem/
    url(r'^printcart/$', biviews.print_items_cart, name='print_item_incart'),
    # ---------------------
    # Django plot
    # ---------------------
    url(r'^plot/testplot1', biviews.simple_test_matplotlib, name='plot_test'),
    url(r'^plot/testplot2', biviews.plot_of_test, name='plot_test2'),
    url(r'^plot/testplot3/(?P<kind>[\d]{1})/$', biviews.mplimage2, name='plot_test3'),
    url(r'^testbtable', biviews.PandasOfView, name='pandas_of'),

    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
