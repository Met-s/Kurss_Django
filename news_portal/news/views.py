from django.shortcuts import render
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, )
from .models import Post
from .forms import PostForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from pprint import pprint


class PostList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.category_type = 'AR'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.category_type == 'NW':
            return super().form_valid(form)
        else:
            html = (f"<html><body><h1>"
                    f"Эта страница для редактирования Новостей.<br>"
                    f"Для редактирования Статей перейдите по адресу "
                    f"/article/int:pk/edit </h1></body></html>")
            return HttpResponse(html)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.category_type == 'AR':
            return super().form_valid(form)
        else:
            html = (f"<html><body><h1>"
                    f"Эта страница для редактирования Статей.<br>"
                    f"Для редактирования Новостей перейдите по адресу "
                    f"/news/int:pk/edit </h1></body></html>")
            return HttpResponse(html)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')

