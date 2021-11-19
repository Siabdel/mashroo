# -*- coding: utf-8 -*-

# Create your views here.
import os, sys, time
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import  redirect, render, reverse, redirect

from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, BaseListView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from blog.forms import BlogForm
from blog.models import Article
from django import forms
from core.taxonomy.models import Category
import datetime



# @permission_required('projects.view_project')
@method_decorator(login_required, 'dispatch')
class AccueilView(ListView):
    """
    Home page Project
    """
    template_name = "siteweb/index.html"
    model = Article

    def get_context_data(self,  **kwargs):
        context = super(AccueilView, self).get_context_data(**kwargs)
        # context['filter_fields'] = self.model.objects.all()


        context['user'] = self.request.user
        context['form'] = form

        if self.request.user.has_perm("projects.change_project"):
            messages.success(self.request, _("j'ai la permission = projects.change_project"))

        return context



#@permission_required('projects.add_project')
@method_decorator(login_required, 'dispatch')
class AddArticleBlog(CreateView):
    template_name = "blog/blog_edit.html"
    form_class = BlogForm
    model = Article

    def get_success_url(self):
        return reverse('article_details', kwargs={'pk' : self.object.pk })

    def get_context_data(self,  **kwargs):
        context = super(AddArticleBlog, self).get_context_data(**kwargs)
        # context['filter_fields'] = self.model.objects.all()
        form = self.get_form()
        form.initial.update({
                             'author' : self.request.user.id,
                             'category' : 1,
                              })

        form.fields['author'].widget = forms.HiddenInput()
        # form upload
        # context['form_file'] = DocumentForm()


        context['user'] = self.request.user
        context['form'] = form

        messages.success(self.request, _("j'ai la permission = projects.change_project"))

        return context


class ArticleDetailBlog(DetailView):
    template_name = "blog/blog_details_clean.html"
    model = Article



class ArticleEditBlog(UpdateView):
    template_name = "blog/blog_edit.html"
    form_class = BlogForm
    model = Article

    def get_success_url(self):
        return reverse('article_details', kwargs={'pk' : self.object.pk })

    def get_context_data(self,  **kwargs):
        context = super(ArticleEditBlog, self).get_context_data(**kwargs)
        # context['filter_fields'] = self.model.objects.all()
        form = self.get_form()
        form.fields['author'].widget = forms.HiddenInput()
        # form upload
        # context['form_file'] = DocumentForm()

        context['user'] = self.request.user
        context['form'] = form
        return context


class ArticleListBlog(ListView):
    template_name = "blog/blog_list.html"
    model = Article


class ArticleDeleteBlog(DeleteView):
    template_name = "blog/article_confirm_delete.html"
    model = Article

    def get_success_url(self):
        return reverse('article_list',  )




class ArticleHomeBlog(ListView):
    template_name = "blog/blog_home.html"
    model = Article
    object_list = None


    def get(self, request, slug, **kwargs):
        context = self.get_context_data(**kwargs)
        ce_mois_ci = datetime.datetime.now().month
        #messages.success(self.request, "filtre = %s "% self.object_list)
        context['object_list'] = self.get_queryset()
        return render(request, self.template_name, context)



    def get_queryset(self):
        try :
            cat = get_object_or_404(Category, slug__icontains=self.kwargs['slug'])
            self.object_list =  Article.objects.filter(category = cat)

        except Exception as err:
            self.object_list = []

        return self.object_list
