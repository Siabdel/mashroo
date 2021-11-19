# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
from django.contrib import admin
from projects import models as pro_models
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.management import get_permission_codename
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
# from core.profile.models import  ProfileUser as Profile
from django.contrib.auth.admin import UserAdmin, User
from core.profile import models as profile_models
from core.taxonomy.models import GDocument, Document


# Register your models here.

# export des données en admin de toutes les table
# def make_planified(modeladmin, request, queryset):
def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    return HttpResponseRedirect("/export/%s/%s" % (ct.pk, ",".join(selected)))

#-----------------
# Project
# ---------------
class TicketAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  pro_models.Ticket._meta.get_fields()]
    list_total.remove( 'tasks')
    list_total.remove('tags')
    # list_total.remove('stream')
    list_total.remove('tagged_items')

    # exclude = ['stream',  ]
    #list_display = list_total
    list_display = ['id', 'title', 'description',   ]



class ProjectAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  pro_models.Project._meta.get_fields()]
    list_total.remove('tags')
    #list_total.remove( 'members')
    #list_total.remove( 'Project_ProfileUser')
    list_total.remove( 'milestone')

    list_display = list_total
    list_display = ['id', 'code',   'title', 'created', 'status', 'description' , 'manager', 'author', 'visibilite' ]
    # exclude = ['stream',  ]
    #autocomplete_lookup_fields = { 'Project_ProfileUser': [['project', 'member']], }



    search_fields = ['title'] # moteur de recherche
    #list_filter  = ('category', )
    # action supplementaires
    actions  = [ 'export_as_json',  'export_as_csv',  'make_closed']

    def export_as_json(modeladmin, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    def export_as_csv(modeladmin, request, queryset):
        # Create the HttpResponse object with the appropriate CSV header.
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
        writer = csv.writer(response)
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.created),
                smart_str(obj.code),
                smart_str(obj.title),
                smart_str(obj.description),
                smart_str(obj.author),
                smart_str(obj.status),
                smart_str(obj.manager),
            ])
        # return HttpResponseRedirect("/export/csv/%s/%s" % (ct.pk, ",".join(selected)))
        return response


    def export_json_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/export/json/%s/%s" % (ct.pk, ",".join(selected)))


    def export_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/export/%s/%s" % (ct.pk, ",".join(selected)))

    def export_csv_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        #return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/export/csv/%s/%s" % (ct.pk, ",".join(selected)))

    def make_planified(self, request, queryset):
        project_updater =  queryset.filter(status='C').update(statut='P')
        #pass
        if project_updater == 1:
            message = "project cloturé"
        else :
            message = "La cloture des projects est réussi "
        self.message_user(request, "%s " % message)



class MilestoneAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  pro_models.Milestone._meta.get_fields() ]
    # list_total.remove( 'stream')
    list_total.remove( 'categories')
    list_total.remove( 'tags')
    #list_total.remove( 'members')
    # list_total.remove( 'milestone_member')
    exclude = ['stream', 'dashboard',  ]
    list_display = list_total
    #list_display = ['id',   ]


admin.site.register(pro_models.Ticket, TicketAdmin)
admin.site.register(pro_models.Project, ProjectAdmin)
admin.site.register(pro_models.Milestone, MilestoneAdmin)
# admin.site.register(models.Project_ProfileUser)


class PartenaireAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'tiers_id', 'tiers_type',
                # ...
            )
        }),
        (_('page/article'), {
            'classes': ('grp-collapse grp-open',),
            'fields': ('content_type', 'object_id', )
        }),
    )
    autocomplete_lookup_fields = { 'generic': [['content_type', 'object_id']], }


class TagsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'tag',
                # ...
            )
        }),
        (_('page/article'), {
            'classes': ('grp-collapse grp-open',),
            'fields': ('content_type', 'object_id', )
        }),
    )
    #
    autocomplete_lookup_fields = { 'generic': [['content_type', 'object_id']], }

from core.taxonomy.models import TaggedItem

admin.site.register(TaggedItem,  TagsAdmin)
admin.site.register(pro_models.Partenaire,  PartenaireAdmin)


class ProfileInline(admin.StackedInline):
    model = pro_models.UProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
    list_select_related = ('profile', )

    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# admin.site.unregister(User)
# admin.site.unregister(User)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'do_title', 'do_description', 'document','file_basename', 'active', 'thumbnail_file', 'initial_name', 'file_type', 'file_size',  )



class MemberAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  pro_models.UProfile._meta.get_fields() ]
    exclude = ['id',  'user', ]
    list_display = list_total
    exclude = ('membership', )
    list_display = ['id', 'user',   'date_naissance', 'photo',   'fonction', 'service', 'language', 'role']


class VtodoAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  pro_models.Vtodo._meta.get_fields() ]
    exclude = [  'user', ]
    list_display = list_total

admin.site.register(pro_models.Vtodo, VtodoAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(profile_models.UProfile, MemberAdmin)
