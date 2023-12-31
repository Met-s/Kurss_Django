from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, )
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import (
    PermissionRequiredMixin
)
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from .filters import PostFilter
from .models import Post, Category, Subscriber
from .forms import PostForm
import logging
from django.views import View
from django.utils import timezone
import pytz


logger = logging.getLogger(__name__)


class PostList(ListView):
    logger.info('INFO')
    model = Post
    ordering = '-post_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def set_timezone(self, request):
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('news')
        else:
            return render(request, 'news.html',
                          {'timezones': pytz.common_timezones})

    def post(self, request):
        request.session['django_timezone'] = request.POST.get('timezone',
                                                              None)
        return redirect('news')


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'
    queryset = Post.objects.all()

    def get_object(self, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
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


class NewsSearch(ListView):
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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_pk = request.POST.get('category_pk')

        category = Category.objects.get(pk=category_pk)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user,
                                      category=category)

        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions}
    )


class Index(View):
    def get(self, request):
        models = Post.objects.all()
        context = {'models': models,
                    'current_time': timezone.localtime(timezone.now()),
                    'timezones': pytz.common_timezones
                    }
        # string = _('Hello World')
        # context = {'string': string}
        return HttpResponse(render(request,
                                   'translation.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('index')
