from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DetailView, DeleteView, ListView, UpdateView)

from .forms import ArticleModelForm
from django.urls import reverse

from .models import Article


class ArticleCreateView(CreateView):
    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()
    # success_url = '/' # we can navigate any where, but we are using the default method get_absolute_url()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    # this is also a navigation method
    # def get_success_url(self):
    #     return '/'


class ArticleUpdateView(UpdateView):
    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ArticleListView(ListView):
    template_name = 'articles/article_list.html'
    queryset = Article.objects.all()  # <blog>/<modelname>_list.html


class ArticleDetailView(DetailView):
    template_name = 'articles/article_details.html'
    # queryset = Article.objects.all()

    # to get a specific article

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)


class ArticleDeleteView(DeleteView):
    template_name = 'articles/article_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def get_success_url(self):
        return reverse('articles:article-list')
