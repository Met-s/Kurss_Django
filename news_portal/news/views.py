from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, )
from .models import Post
from .forms import PostForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from .filters import PostFilter
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)


class PostList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    # raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.category_type = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.add_post'
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


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.add_post'
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


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.add_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')


class NewsSearch(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
