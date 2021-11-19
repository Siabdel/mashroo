from django.contrib import admin
from django.db import models

# Register your models here.
from blog import models as blog_models
from mdeditor.fields import MDEditorWidget


class BlogAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  blog_models.Article._meta.get_fields() ]
    # prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }
    #exclude = [  '', ]
    list_display = list_total


admin.site.register(blog_models.Article, BlogAdmin)
