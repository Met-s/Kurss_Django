Зарегистрировал модели

news/admin.py

from django.contrib import admin
from .models import Category, Post

admin.site.register(Category)
admin.site.register(Post)
----------------------------------
В данный момент нам нужен дженерик ListView, который выводит список объектов
модели, используя указанный шаблон.

news/views.py

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView
from .models import Post

class PostList(ListView):
    # Указываем модель объекты которой будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'post_date'
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно
    # пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

Вот так можно использовать дженерик ListView для вывода списка товаров:
 1.Создаём свой класс, который наследуется от ListView
 2.Указываем модель, из которой будем выводить данные.
 3.Указываем поле сортировки данных модели (необязательно)
 4.Записываем название шаблона.
 5.Объявляем, как хотим назвать переменную в шаблоне.
-------------------------------
Настраиваем адрес:
Для этого необходимо настроить пути в файле urls.py. При выполнении
инициализации нового приложения Django не создавал этот файл в нашей директории,
поэтому мы создадим его сами.
news/urls.py

from django.urls import path
from .views import PostList

urlpatterns = [
    # path - означает ПУТЬ
    # В данном случае путь ко всем товарам останется пустым
    # Т.к. объявленное представление является классом, а Django ожидает
    # функцию, надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostList.as_view()),
]
Задали ПУТЬ к нашему представлению
-----------------------------------
Вывод из БД. Для этого в главном файле urls.py в котором подключали flatpages
нужно сделать так, чтобы он автоматически включал все наши адреса из приложения
 и добавлял к нему префикс products.

django_d3/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
    # подключались к главному приложению с префиксом products/.
    path('news/', include('news.urls')),
]
------------------------------------
Настроил settings.py

'django.contrib.sites',
'django.contrib.flatpages',
'simpleapp'

SITE_ID = 1

'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

'DIRS': [os.path.join(BASE_DIR, 'news/templates/news')],
или
'DIRS': [BASE_DIR / 'news/templates/news'],

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
---------------------------------------
Применил миграции

py manage.py makemigrations
py manage.py migrate

Создал супер юзера

py manage.py createsuperuser
---------------------------------------
Добавляем шаблон default.html

news/templates/news/flatpages/default.html  # Так по правилам
---------------------------------------
Добавил папку news_portal/static и изменил шаблон в default.html
---------------------------------------
добавление панели в админке: для зарегистрированных пользователей
создадим файл django_d3/flatpages/admin.py

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
        'classes': ('collapse',),
        'fields': (
            'enable_comments',
            'registration_required',
            'template_name',
         ),
        }),
    )
# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

Нужно зарегистрировать новое приложение Flatpages в настройках settings.py
'fpages'
---------------------------------------
Несмотря на то, что мы видим довольно неказистый текст (пока что),всё же здесь
присутствуют наши товары.

Если переложить всё, что сделали на MVC, то получится:
1. Model - сделали модели для товаров и категорий в models.py
2. View - написали темплейт в news.html
3. Controller - настроили представление с логикой вывода списка товаров в views.py
Вот все части MVC и сложились в нашем приложении.
---------------------------------------


views.py
Фильтр цена ниже 500
class ProductsList(ListView):
    # Указываем модель объекты которой будем выводить
    # model = Product
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'name'
    queryset = Product.objects.filter(
        price__lt=500
    )
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно
    # пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
----
Можно добавить сортировку и по имени
queryset = Product.objects.filter(
        price__lt=900
    ).order_by('-name')



---------------------------------------
Добавил в views.py class PostDetail(DetailView):
для отображения одного продукта
---------------------------------------
Добавляем адрес в news/urls.py.
Адрес будет немного отличаться. В него нужно добавить идентификатор товара,
который хотим получить.
    # pk - это первичный ключ товара, который будет выводиться у нас в шаблон
    # int - указывает на то, что принимаются только целочисленные значения
path('<int:pk>', PostDetail.as_view()),
---------------------------------------
Добавляем новый шаблон для вывода одного товара по id
news_portal/news/templates/news/post_detail.html
---------------------------------------
Подытожим
1. Добавил новое представление в view.py
2. Зарегистрировал представление в urls.py на путь, который содержит
    целочисленный идентификатор объекта.
3. Добавил новый шаблон в templates/news для представления.
---------------------------------------------------------
Фильтр (truncatechars:21) в шаблоне: отрезает 20 символов и добавляет ...
Добавил условие if, и цикл для вывода статей

{% block content %}
<h1>Все статьи</h1>
<hr>
{% if news %}
    {% for post in news %}
        {{ post.post_title }}

        {{ post.post_text|truncatechars:21}}
        <hr>
    {% endfor %}
{% else %}
    <h1>Извините на данный момент статей нет</h1>
{% endif %}
{% endblock content %}

Фильтр в шаблоне: отрезает 2 слова и добавляет ...
<td>{{ product.description|truncatewords:2 }}</td>

Фильтры очень похожи на методы или функции и имеют примерно следующий синтаксис:
<переменная>|<название метода>:<аргументы>
---------------------------------------
Добавил сортировку в views.py свежая статья вверху
class PostList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news.html'
    context_object_name = 'news'
---------------------------------------
Изменил показ формат даты и статьи

1. Импортировал модуль datetime, чтобы получить текущую дату
2. Переопределил метод get_context_data, добавив две переменные, которые будут
доступны в шаблоне.

views.py
class PostList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news.html'
    context_object_name = 'news'

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
---------------
post_detail.html
{% block content %}
<h1>Одна статья</h1>
<hr>
{{ post_detail.post_date|date:'d M Y' }}
<br>
{{ post_detail.post_title }}
<br>
{{ post_detail.post_text }}
<hr>
{% endblock content %}
----------------
 # Используем переданную из представления переменную post_date и применяем
    к ней фильтр data. По назначению этот фильтр очень похож на метод
    strftime у объекта datetime в Python - вывод времени в указанном формате.

news.html
{% block content %}
<h1>Все статьи</h1>
<hr>
{% if news %}
    {% for post in news %}
        {{ post.post_title }}
        <br>
        {{ post.post_date|date:'d M Y'}}
        <br>
        {{ post.post_text|truncatechars:21}}
        <hr>
    {% endfor %}
{% else %}
    <h1>Извините на данный момент статей нет</h1>
{% endif %}
{% endblock content %}
---------------------------------------
Количество всех новостей

{{ news|length }}
---------------------------------------
Собственный фильтр

@register.filter()
def currency(value):
    """
    value: значение, к которому нуо применить фильтр
    """
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} P'
---------------------------------------
Декоратор register.filter() указывает Django, что нужно запомнить про
существование нового фильтра. Название фильтра по умолчанию берётся равным
названию функции,то есть в шаблоне можно писать
{{ post.post_text|truncatewords:21|censor}}.
Можно самим назвать фильтр. Например: register.filter(name='censor_word'),
а название функции не менять, тогда в шаблоне пишем
{{ post.post_text|truncatewords:21|censor_wod}}.
-------------------
После добавления файла с новыми фильтрами, нужно перезагрузить Django-сервер.
----------------
Просто взять и указать фильтр в шаблоне не получится.
Нужно подключить свои фильтры в шаблоне.
Сделать это можно с помощью указания тега
{% load censor_filters %}
Где custom_filters - это название файла с нашим фильтром.
---------------------------------------
ПАГИНАЦИЯ

news/views.py

lass PostList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news.html'
    context_object_name = 'news'
 Добавил
    paginate_by = 10
--------------
templates/news/news.html

Добавил ссылки на следующие и предыдущие страницы

{% else %}
    <h1>Извините на данный момент статей нет</h1>
{% endif %}
{% if page_obj.has_previous %}
    <a href="?page=1">1</a>
    {% if page_obj.previous_page_number != 1 %}
    ...
    <a href="?page={{ page_obj.previous_page_number }}">{{ page_obj.previous_page_number}}</a>
    {% endif %}
{% endif %}
{{ page_obj.number }}
{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">{{ page_obj.next_page_number }}</a>
    {% if paginator.num_pages != page_obj.next_page_number %}
    ...
    <a href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a>
    {% endif %}
{% endif %}
{% endblock content %}
---------------------------------------
Создание новости
Создал форму

news/forms.py

from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_category',
            'post_title',
            'post_text'
        ]
------------
Создал шаблон

templates/news/news_create/html

{% extends 'flatpages/default.html' %}
{% block content %}
<h1>Создание новости</h1>
<hr>
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save" />
</form>
{% endblock content %}
--------------
Добавил представление

news/views.py

from django.views.generic import (
    ListView, DetailView, CreateView)

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)
-------------
Добавил url
news/urls.py

from .views import (PostList, PostDetail, NewsCreate)
path('news/create/', NewsCreate.as_view(), name='news_create'),
-------------
Всё работает но есть нюанс.
Мы увидим форму но после её отправки, получим ошибку
"ImproperlyConfigured at /products/create/
No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model."

Проблема в том, что Django не знает, какую страницу нужно открыть после создания
товара. И как видно по описанию, можем убрать проблему, добавив метод
get_absolute_url в модель. model Post

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

---------------
Используем спец- функцию reverse, которая позволяет указывать не путь
вида /news/..., а название пути. Если вернуться к описанию путей в urls.py,
то увидим что мы добавили значения для аргументов name. Такой механизм обращения
удобен тем, что если мы захотим изменить пути, прийдётся вносить меньше
изменений в код, а значит, меньше вероятность пропустить какое-то место и
получить баг.

news/urls.py

rom django.urls import path
from django.views.generic import (
    ListView, DetailView, CreateView)
urlpatterns = [
    # path - означает ПУТЬ
    # В данном случае путь ко всем товарам останется пустым
    # Т.к. объявленное представление является классом, а Django ожидает
    # функцию, надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.

    path('', PostList.as_view()),

    # pk - это первичный ключ товара, который будет выводиться у нас в шаблон
    # int - указывает на то, что принимаются только целочисленные значения

    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create')
]
Здесь выводится название в таком же виде, как описано в методе __str__
в модели Post.
GET и POST - запросы работают по-разному. Главное отличие заключается в способе
передачи данных.
Для передачи информации в GET-запросах используется query string,
а в POST- тело запроса.
---------------------------------------
Создание Статьи
Форма та же что и для новости
---------
Создал шаблон

templates/news/article_create/html

{% extends 'flatpages/default.html' %}
{% block content %}
<h1>Создание статьи</h1>
<hr>
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save" />
</form>
{% endblock content %}
-----------
Добавил представление

news/views.py

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=True)
        post.category_type = 'AR'
        return super().form_valid(form)
------------
Добавил url
news/urls.py

from .views import (PostList, PostDetail, NewsCreate, ArticleCreate)

path('articles/create/', ArticleCreate.as_view(), name='article_create')
---------------------------------------
Добавил редактирование

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
---------------------------------------
Добавил удаление

class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
---------------------------------------
Добавил показ категории в шаблон

{% extends 'flatpages/default.html' %}
{% load censor_filters %}

{% block title %}
Post
{% endblock title %}

{% block content %}
<h1>Одна статья</h1>
<hr>
{{ post_detail.post_title }}
<br>
    {% for i in post_detail.post_category.all %}
        {{ i.category_name }}
    {% endfor %}
<br>
{{ post_detail.post_text|censor }}
<br>
{{ post_detail.post_date|date:'d M Y' }}
<hr>
{% endblock content %}
---------------------------------------
Добавил Фильтр
new/filters.py
from django_filters import FilterSet
from .models import Post, PostCategory


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'postcategory__category_through': ['exact'],
            'post_date': ['lt']
        }
--------------
Зарегистрировал фильтр в settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'news',
    'accounts',
    'django_filters',
]
--------------
Создал шаблон
templates/news/news_search.html

{% extends 'flatpages/default.html' %}


{% block title %}
News_Search
{% endblock title %}

{% block content %}
<h1>Поиск статьи</h1>
    <form action="" method="get">
        {# Переменная которую передали через контекст, может сгенерировать нам форму с полями #}
        {{ filterset.form.as_p }}
        {# Добавим кнопку отправки данных формы #}
        <input type="submit" value="Найти" />
    </form>
<hr>
{% if news_search|length %}
    {% for post in news_search %}
        {{ post.post_title }}
        <br>
        {{ post.category_type }}
            {% for cat in post.post_category.all %}
                {{ cat.category_name }}
                <br>
            {% endfor %}

        {{ post.post_date|date:'d M Y'}}
        <br>
        {{ post.post_text|truncatewords:5}}
        <hr>
    {% endfor %}
{% else %}
    <h1>Извините на данный момент статей нет</h1>
{% endif %}

{% if page_obj.has_previous %}
    <a href="?page=1">1</a>
    {% if page_obj.previous_page_number != 1 %}
    ...
    <a href="?page={{ page_obj.previous_page_number }}">{{ page_obj.previous_page_number}}</a>
    {% endif %}
{% endif %}

{{ page_obj.number }}

{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">{{ page_obj.next_page_number }}</a>
    {% if paginator.num_pages != page_obj.next_page_number %}
    ...
    <a href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a>
    {% endif %}
{% endif %}

{% endblock content %}
----------------------------
Создал форму
news/forms.py

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_category',
            'post_title',
            'post_text'
        ]
------------------
Написал представление
from .filters import PostFilter

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
--------------
Прописал путь
news/urls.py

from .views import (PostList, PostDetail, NewsCreate, ArticleCreate,
                    NewsUpdate, ArticleUpdate, NewsDelete, NewsSearch)

path('news/search/', NewsSearch.as_view(), name='news_search'),
---------------------------------------
Чтобы заполненная форма фильтра не пропадала на других страницах
templatetags/custom_tags.py

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
--------------
добавил его в шаблон
news_search.html

{% load custom_tags %}

{% else %}
    <h1>Извините на данный момент статей нет</h1>
{% endif %}

{% if page_obj.has_previous %}
    <a href="?{% url_replace page=1 %}">1</a>
    {% if page_obj.previous_page_number != 1 %}
    ...
    <a href="?{% url_replace page=page_obj.previous_page_number %}">{{ page_obj.previous_page_number}}</a>
    {% endif %}
{% endif %}

{{ page_obj.number }}

{% if page_obj.has_next %}
    <a href="?{% url_replace page=page_obj.next_page_number %}">{{ page_obj.next_page_number }}</a>
    {% if paginator.num_pages != page_obj.next_page_number %}
    ...
    <a href="?{% url_replace page=page_obj.paginator.num_pages %}">{{ page_obj.paginator.num_pages }}</a>
    {% endif %}
{% endif %}

{% endblock content %}
---------------------------------------
Добавил собственную проверку на валидность
forms.py
from django.core.exceptions import ValidationError
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_category',
            'post_title',
            'post_text'
        ]
    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get("post_title")
        if post_title is not None and len(post_title) < 20:
            raise ValidationError({
                "post_title": "Название не может быть меньше 20 символов."
            })
        post_text = cleaned_data.get('post_text')
        if post_text == post_title:
            raise ValidationError(
                "Название не должно совпадать с текстом статьи."
            )
        return cleaned_data
---------------------------------------
D_5
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Добавил условие с выбором редактирования статья или новость
news.html

 <td>
    {% if post.category_type == 'NW' %}
    <a href="{% url 'news_edit' pk=post.id %}">Редактировать</a>
    <a href="{% url 'post_delete' pk=post.id %}">Удалить</a>
    {% else %}
    <a href="{% url 'article_edit' pk=post.id %}">Редактировать</a>
    <a href="{% url 'post_delete' pk=post.id %}">Удалить</a>
    {% endif %}
</td>
---------------------------------------
Добавил проверку на авторизацию

news/views.py

from django.contrib.auth.mixins import LoginRequiredMixin

class NewsCreate(LoginRequiredMixin, CreateView):
    raise_exception = True   # Вот здесь
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
---------
news.html

<td>
    {% if request.user.is_authenticated %}

    {% if post.category_type == 'NW' %}
    <a href="{% url 'news_edit' pk=post.id %}">Редактировать</a>
    <a href="{% url 'post_delete' pk=post.id %}">Удалить</a>
    {% else %}
    <a href="{% url 'article_edit' pk=post.id %}">Редактировать</a>
    <a href="{% url 'post_delete' pk=post.id %}">Удалить</a>
    {% endif %}

    {% endif %}
</td>
----------
Теперь неавторизованные пользователи не увидят ссылок для
редактирования и удаления статей.
---------------------------------------
Добавил шаблон для вывода сообщения для ошибки 403
news/templates/403.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ошибка 403</title>
</head>
<body>
<h1>У вас нет доступа к этой странице</h1>
</body>
</html>
----------
Для проверки работы шаблона, проверку проверку на авторизацию пришлось
за комментировать

<td>
    {# {% if request.user.is_authenticated %}#}
---------------------------------------
Форма для входа (регистрации) пользователя
news/templates/registration/login.html

{% extends 'flatpages/default.html' %}

{% block content %}
    <form method="post" action="{% url 'login' %}">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Войти">
        <input type="hidden" name="next" value="{{ next }}">
    </form>
{% endblock content %}
----------
Настроил так чтобы после входа нас перенаправляло на страницу с постами
добавим строчку в
settings.py

LOGIN_REDIRECT_URL = "/news"  # Добавил ссылку на страницу для
    перенаправления после входа пользователя
---------------------------------------
Регистрация
!!!!!!!!!!!!!!!!
Создал отдельное приложение для регистрации пользователей
python manage.py startapp accounts
-----------------
Добавил форму регистрации по имени и email

Создал форму в:
accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
--------------
Создал представление
accounts/views.py

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.urls import reverse_lazy


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('news')
    template_name = 'registration/signup.html'
--------------
Добавим шаблон:
news/templates/registration/signup.html

{% extends 'flatpages/default.html' %}

{% block content %}
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Sing up">
  </form>
{% endblock content %}
--------------
Подключил urlpatterns, чтобы регистрация стала доступна на сайте.
Для этого создал и заполнил файл urls.py в новом приложении.
accounts/urls.py

from django.urls import path
from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]
---------------
Подключил urls приложения account в главном приложении django_d4.
news_portal/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/', include('accounts.urls')), # вот это
]
---------------
После регистрации нас перенаправит на страницу news с постами.
---------------------------------------
OAuth установил пакет
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
pip install django-allauth
---------------
settings.py

В установленных приложениях необходимо убедиться в наличии
некоторых встроенных приложений Django, которые добавляют:

• пользователей - 'django.contrib.auth',
• сообщения - 'django.contrib.messages',
• настройки сайта - 'django.contrib.sites',

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'news',
    'accounts',
    'django_filters',

   # Добавил

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex'
]
MIDDLEWARE = [
    .........
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
   # Без этой строчки миграции не проходят

    'allauth.account.middleware.AccountMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'news/templates/news'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
              # allauth обязательно нужен этот процессор

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

Чтобы после регистрации или входа перенаправляло на страницу news с постами

LOGIN_REDIRECT_URL = "/news"

Добавил раздел

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
-------
После модификации файла настроек обязательно нужно выполнить миграцию.
Иначе необходимые модели из подключенных приложений не создадутся в нашей БД.
-------------------------------------------------
Регистрация по email и паролю
!!!!!!!!!!!!!

В файл настроек проекта внесём дополнительные параметры, в которых укажем обязательные
и необязательные поля.

settings.py

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
---------------
После этих настроек, нужно заглянуть в главный файл URL и внести изменения,
чтобы по accounts было доступно только приложение allauth.

news_portal/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
 # Эти два нам больше не нужны
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),

  # Вот это
    path('accounts/', include('allauth.urls')),
]
---------------
Теперь для регистрации необходимо ввести только email и пароль.
---------------------------------------
Регистрация и вход через Yandex
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Добавил настройки сайта, которые требуются для allauth

1. Войдём в панель администратора
    • http://127.0.0.1:8000/admin/
    • вкладка Sites - отредактировать объект Site
        Domain name: 127.0.0.1
        Display name: example.com # и сохранить
-------------
Создал новый My apps, но яндекс отказался его принимать, выдал сообщение о
подозрительном сайте, поэтому использовал старый который применял при прохождении
модуля. И всё заработало!
------------
2. Регистрируем приложение в Yandex для работы с сервисом
    • Преходим https://oauth.yandex.com/client/new и заполняем обязательные поля
        • General
            • Service name - SkillFactoryTest
        • Platforms
            • Choose at least one platform
                х Web setvices
                  Redirect URI
                  URL the user is redirected to after allowing or denying access to the app
                     http://127.0.0.1:8000
                     http://127.0.0.1:8000/accounts/yandex/login/callback
        • Data access
            To add a permission, enter its name
                Permission name # поле для выбора по каким полям проходит
                регистрация
                Access to email address # у нас заявлено что по email
                login:email
                - # и по username
                Access to username, first name and surname, gender
                login:info
3. Подтверждаем создание приложения и видим секретные данные. Они нам понадобятся
    для регистрации провайдера в нашем Django проекте.
4. Секретные данные теперь нужно перенести в наше приложение.
    Открываем : http://127.0.0.1:8000/admin/socialaccount/socialapp/add/
Или вот так в админке:
Home › Social Accounts › Social applications › Add social application

 Provider: Yandex
    Name: любое имя например Yandex
    Client id: ID с страницы приложения Yandex. Поле: "ClientID"
    Seret key: Password с страницы приложения Yandex. Поле: "Client secret"
    Sites переносим единственный сайт в Chosen sites
---------------
И сохраняем.
---------------
Группы пользователей
!!!!!!!!!!!!!!!!!!!!!!!!!!
Через панель администратора самый простой способ
Панель администратора - Groups - Add group

Создал группу authors.
Выдал ей права на создание и редактирование статей.
И создал группу users, для того чтобы новые пользователи при регистрации
автоматически добавлялись в эту группу.
И сохранил.
---------------
Для этого изменим форму SignupForm полностью переписав файл
accounts/forms.py

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        users = Group.objects.get(name="users")
        user.groups.add(users)
        return user
---------------
Чтобы allauth распознал форму как ту,что должна выполняться вместо формы
по умолчанию, добавить строчку в файл настроек проекта
news_portal/settings.py

ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignUpForm"}
---------------
Добавление группы будет работать только для пользователей, которые регистрируются
с помощью почты и пароля.
---------------
Проверка прав доступа в представлении
!!!!!!!!!!!!!!!!!!!!!

news/view.py

from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post' # Добавляем проверку
    # raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
---------------
Проделываем со всеми представлениями где нужна проверка.
---------------------------------------
По заданию D_5 выполнил.
---------------------------------------
В проект не добавлял в задание это не входит
---------------------------------------
Проверка прав в шаблоне
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Чтобы скрыть лишние ссылки, можно установить проверки в самом шаблоне:
templates/news/news.html
---------------------------------------
D_6
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Создал приветственное письмо новому пользователю с ссылкой на сайт, письмо
приходит на почту при успешной регистрации.
-------------
Добавил блок настроек работы с почтой

settings.py

# console - будет печатать в консоль
# smtp - отправляет на почту

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "si-mart"  # Без @yandex.ru
EMAIL_HOST_PASSWORD = email_host_password  # config.py
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "si-mart@yandex.ru"
-------------
Отправка письма в текстовом и в HTML формате
Переписал форму регистрации

accounts/forms.py

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives

class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        users = Group.objects.get(name="users")
        user.groups.add(users)
        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'нашем новостном портале! Добро пожаловать:'
            f'<a href="http://127.0.0.1:8000/news">На сайт</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        return user
-------------
Теперь пользователь после регистрации получает приветственное письмо с ссылкой
на страницу со всеми новостями.
---------------------------------------
Подписка пользователей на категории
-------------
Создал таблицу,в БД, чтобы хранить список категорий, на которые подписан
пользователь.

news/models.py

class Subscriber(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE,
                                 related_name='subscriptions')
-------------
Добавил переменную  в
settings.py

SITE_URL = "http://127.0.0.1:8000"
-------------
Написал Функцию, которая отправляет письмо. Пользователю подписавшемуся на
категорию поста, при создании поста в этой категории.

news/signals.py

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory

# Отправляет письмо пользователю text/html

def send_notification(preview, pk, post_title, subscribers):
    html_content = render_to_string(
        'post_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# Собирает email-ы подписчиков на категорию после создании статьи когда ей
# присвоится категория

@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.category_sub.all()
        subscribers = [s.user.email for s in subscribers]
        send_notification(instance.preview(), instance.pk, instance.post_title,
                          subscribers)
-------------
Просто так сигналы не начнут работать. Нам нужно выполнить этот модуль (файл с
Python-кодом). Для этого подойдёт авто-созданный файл apps.py в нашем
приложении. В этом файле есть класс с настройками нашего приложения. Добавим в
него метод ready, который выполнится при завершении конфигурации нашего
приложения news. В самом методе импортируем сигналы, таким образом
зарегистрировав их.

news/apps..py

from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
-------------
Создал шаблон сообщения которое будет отправляться подписчику

templates/news/post_email.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h2>Здравствуйте! Появилась новая статья в категории на которую вы подписаны</h2>
<p>{{ text }}</p>
<h3><a href="{{ link }}">Читать полностью</a></h3>
</body>
</html>
---------------------------------------
Создал еженедельную рассылку пользователям в пятницу 18:00
Установил django-apscheduler
pip install django-apscheduler
------------------
Зарегистрировал в settings
django_apscheduler

Добавил в settings

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a' # формат даты
APSCHEDULER_RUN_NOW_TIMEOUT = 25 # продолжительность выполнения 25 сек.
------------------

------------------

------------------
Это приложение использует модели, поэтому нужно выполнить миграции для создания
таблиц в БД
python manage.py makemigrations
python manage.py migrate
---------------
Теперь как написано в документации, создадим свою Джанго-команду для
выполнения периодических задач.
    Путь до файла с командой очень важен. Файл должен лежать в одном из наших
приложений, по пути management/commands.
А название файла будет идентично тому как мы хотим назвать КОМАНДУ.
---------------
Получается при создании файла
news/management/commands/runapscheduler.py у нас станет доступна команда
python manage.py runapscheduler.
---------------
Создал файл:
news/management/commands/runapscheduler.py

import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category, Subscriber
from news_portal import settings

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)

    # имена категорий, постов вышедших за неделю
    categories = set(posts.values_list('post_category__category_name', flat=True))
    # --------------------------------------------------
    # подписчики с категориями на которые они подписаны
    subscribers: list[str] = []
    subscribers = set(Subscriber.objects.filter(
        category__category_name__in=categories))

    # список категорий у подписчиков
    subscribers_cat = set(s.category for s in subscribers)

    # отфильтровал посты по категориям, остались только те которые есть в
    списке подписчиков
    pos = set(posts.filter(post_category__category_name__in=subscribers_cat))

    # вытащил email-ы подписчиков на которые будет осуществляться рассылка
    subscriber = set(s.user.email for s in subscribers)

    # --------------------------------------------------
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': pos,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# ------Отладка------------------------------------------

    print(f'DOROTY DAUN : ')

    print(f'categories : {categories}')
    print(f'subscribers : {subscribers}')

    print(f'subscribers_cat : {subscribers_cat}')
    print(f'subscriber : {subscriber}')
# ------------------------------------------------


# @util.close_old_connections
def delete_old_job_executions(max_age=604_800):
#     """
#     Это задание удаляет записи выполнения заданий APScheduler старше
#     максимального возраста 'max_age' из БД.
#     Это помогает предотвратить заполнение БД старыми историческими данными,
#     записи которые больше не нужны.
#     : param max_age: максимальная продолжительность хранения исторических
#     записей выполнения заданий. По умолчанию 7 дней.
#     """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            # day_of_week="fri", hour="18", minute="00"  пятница 18:00  wed
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

---------------
Создал шаблон письма с ссылками на статьи, которое будет отправляться
пользователю

templates/news/weekly_post.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h2>Здравствуйте! В категории на которую вы
    подписаны, вышли новые статьи за неделю.</h2>
<ul>
    {% for post in posts %}
        {% for cat in post.post_category.all %}
                       {{ cat.category_name }} :
                    {% endfor %}

        {{ post.preview }}


    <li>
        <a href="{{ link }}{{post.get_absolute_url}}">{{ post.post_title}}</a>
    </li>

    {% endfor %}
</ul>
</body>
</html>
---------------
Для запуска apscheduler:
Открыть второй терминал и набрать команду
python manage.py runapscheduler
---------------
Для тестирования и настройки:
scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/5"), # будет запускаться каждые 5 сек
            # day_of_week="fri", hour="18", minute="00"  пятница 18:00  wed
            id="my_job",
            max_instances=1,
            replace_existing=True,

В settings.py

console - выводит в консоль
smtp - отправляет email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' -отправляет email
---------------------------------------
D_7
===============================================================================
Для использования асинхронного взаимодействия в Django-проектах проверенным
временем решением является библиотека Celery.
Установил Celery
---------------
pip install celery
---------------
Создал файл:
news_portal/news_portal/celery.py
celery.py

import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'news_portal.settings')
app = Celery('news')
app.config_from_object('django.conf:settings',
                       namespace='CELERY')
app.autodiscover_tasks()
---------------
• В первую очередь мы импортируем библиотеку для взаимодействия с операционной
    системой и саму библиотеку Celery.
• Второй строчкой мы связываем настройки Django с настройками Celery через
    переменную окружения.
• Далее мы создаем экземпляр приложения Celery и устанавливаем для него файл
    конфигурации. Мы также указываем пространство имен, чтобы Celery сам
    находил все необходимые настройки в общем конфигурационном файле
    settings.py. Он их будет искать по шаблону «CELERY_***».
• Последней строчкой мы указываем Celery автоматически искать задания в файлах
    tasks.py каждого приложения проекта.
---------------
Добавил в файл __init__.py
news_portal/news_portal/__init__.py
__init__.py

from .celery import app as celery_app

__all__ = ('celery_app',)
---------------
На этом базовые настройки Celery окончены.
---------------------------------------
Установил Redis
---------------
Redis установлен локально
Чтобы запустить
redis-server
redis-cli
---------------
Проверка работы redis
127.0.0.1:6379> ping
если всё хорошо получим ответ
PONG
---------------
Команды redis
127.0.0.1:6379> info  # показывает информацию о бд
db0:keys=61,expires=58,avg_ttl=25611094 # db0 - это номер БД
127.0.0.1:6379> flushdb  # очищает текущую БД
redis-cli -n 8 flushdb # очищает  БД с номером восемь
redis-cli flushall # добавляет всю БД
---------------
Настроил поддержку Redis в Python и Celery

pip3 install redis
pip3 install -U "celery[redis]"
---------------
Сначала запускаем- redis-server
Затем запускаем- redis-cli
Работает
---------------
Добавил настройки в конфигурацию проекта (settings.py)
settings.py

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
---------------------------------------
Если вы используете Redis Labs, то переменные CELERY_BROKER_URL и
CELERY_RESULT_BACKEND должны строиться по шаблону:

redis://логин:пароль@endpoint:port
где endpoint и port вы также берёте из настроек Redis Labs.

Также обратите внимание, что Celery с версией выше 4+ не поддерживается Windows.
Поэтому если у вас версия Python 3.10 и выше, запускайте Celery, добавив в
команду флаг: --polo=solo.

celery -A news_portal worker -l INFO --pool=solo
---------------------------------------
Запускаем:
В первом терминале вводим команду:

python3 manage.py runserver
---------------
Во втором:

celery -A news_portal worker -l INFO --pool=solo
---------------
 -------------- celery@DESKTOP-IH4T6KH v5.3.4 (emerald-rush)
--- ***** -----
-- ******* ---- Windows-10-10.0.19045-SP0 2023-10-18 15:14:46
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         news:0x2be4b5e3310
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     redis://localhost:6379/
- *** --- * --- .> concurrency: 4 (solo)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
---------------
Всё работает!
==============================================================================
Восстановил  GitHab:
Установил приложения:
pip install django
django-apscheduler
pip install celery
pip install redis
pip install -U "celery[redis]"
value
django-filter
django-allauth
==============================================================================
Всё работает!!!
---------------------------------------
Реализовал рассылку email, подписчикам после создания статьи.
---------------
Создал задачу:
tasks.py

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post, Subscriber, PostCategory
from news_portal import settings


@shared_task
def send_email_task(pk):
    posts = Post.objects.get(pk=pk)
    categories = posts.post_category.all()
    subscribers: list[str] = []
    for category in categories:
        subscribers += category.category_sub.all()
    subscribers = [s.user.email for s in subscribers]

    html_content = render_to_string(
        'post_email.html',
        {
            'text': posts.preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=posts.post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
---------------
Переписал файл signals.py.
signals.py

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_email_task


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_email_task.delay(instance.pk)
---------------
По факту взял сигнал и разложил его.
Обработав связь m2m_changed.
---------------------------------------
Реализовал еженедельную рассылку с последними новостями (каждый понедельник в
8:00 утра).
Для этого переделал функцию из runapsheduler.py
---------------

news/tasks.py

from datetime import datetime, timedelta

@shared_task
def post_weekly_notification():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(
        posts.values_list('post_category__category_name', flat=True))
    # --------------------------------------------------
    # subscribers: list[str] = []
    subscribers = set(Subscriber.objects.filter(
        category__category_name__in=categories))
    subscribers_cat = set(s.category for s in subscribers)
    pos = set(posts.filter(post_category__category_name__in=subscribers_cat))
    subscriber = set(s.user.email for s in subscribers)
    # --------------------------------------------------
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': pos,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
---------------
Добавил задачу в
celery.py

from celery.schedules import crontab

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.post_weekly_notification',
        'schedule': crontab(hour='8', minute='0', day_of_week='monday'),
    }
}
---------------------------------------
Для запуска задач по расписанию,необходимо запускать Celery с флагом -B,
который позволяет запускать периодические задачи:

celery -A news_portal worker -l INFO -B
-----------
Для запуска периодических задач на Windows запустите в разных окнах терминала:

celery -A news_portal worker -l INFO pool=solo
и
celery -A news_portal beat -l INFO pool=solo #  c (pool=solo) выдаёт ошибку
    без него всё работает
---------------------------------------
==============================================================================
D_8                                                                        D_8
==============================================================================
Кеширование
Настройки:
------------
Создал папку для кеширования:
news_portal/cache_files
------------
Добавил настройки в
settings.py
import os

CACHES = {
    'default': {
        'BACKEND':
            'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}
------------
Добавьте кэширование на страницы с новостями (по 5 минут на каждую) и на
главную страницу (одну минуту).
Изменил в:
news_portal/news/urls.py

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='news'),  # 1m
    path('<int:pk>', cache_page(60*5)(PostDetail.as_view()),
         name='post_detail'),  # 5m
    path('create/', NewsCreate.as_view(), name='news_create'),
---------------------------------------
В шаблонах постарайтесь кэшировать все навигационные элементы
(меню, сайдбары и т. д.). Количество кэшируемого времени  600 сек.
news_portal\news\templates\news\flatpages\default.html

<!DOCTYPE html>
<html lang="en">
{% load cache %}
{% cache 600 header %}

    <head>
    ........
    </head>
{% endcache %}
........
</style>
{% cache 600 body %}
    <body>
    ........
        </nav>
{% endcache %}
        <!-- Page content -->
        ......
</html>
---------------------------------------
Подробнее здесь:
Django’s cache framework | Django documentation | Django
https://docs.djangoproject.com/en/3.1/topics/cache/
---------------------------------------
ПЕРЕДЕЛАЛ!
------------
Убрал кеширование из urls.py

Сделал его в шаблонах:
news/templates/news/news.html  1 минута

{% extends 'flatpages/default.html' %}
{% load censor_filters %}
{% load cache %}


{% block title %}
Все посты
{% endblock title %}

{% block content %}
{% cache 60 content %}
<h1>Все статьи</h1>
.....
{% endcache %}
{% endblock content %}

------------
news/templates/news/post_detail.html  5 минут

{% extends 'flatpages/default.html' %}
{% load censor_filters %}
{% load cache %}

{% block title %}
    Post
{% endblock title %}

{% cache 300 content %}
    {% block content %}
....
        <hr>
    {% endblock content %}
{% endcache %}
---------------------------------------
Кэширование на низком уровне
Кеширование для статей.
Пока статья не изменилась, она должна сохраняться в кэше.
---------------
Добавил в news/views.py

from django.core.cache import cache

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'

queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj
---------------
news_portal/news/models.py

from django.core.cache import cache

class Post(models.Model):
    news = 'NW'
    article = 'AR'

    CATEGORY_CHOICES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES,
                                     default=article)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.SmallIntegerField(default=0)

   ................ добавил метод сохранения (перезаписи в БД)..........
    def get_absolute_url(self):
        return f'/news/{self.pk}'
        # return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')
---------------
Всё работает.
Но есть один нюанс:
С запущенным  Redis - сайт работает быстро
Без Redis - тормозит при создании статьи
---------------------------------------
==============================================================================
D_9                                                                     D_9
Авто проверка кода
==============================================================================
Flake8 и PyLint

Случай использования	Flake8	            PyLint
Установка	            pip install flake8	pip install pylint
Получить справку	    flake8 --help	    pylint
Проанализировать        flake8 <filename>	pylint <filename>
конкретный файл или
модуль
---------------
Установил
pip install flake8
pip install pylint
---------------------------------------
Создаёт файл со списком пакетов для последующей установки
pip freeze > requirments.txt
Устанавливаем все пакеты из файла
pip install -r requirments.txt
---------------

---------------


---------------------------------------


---------------
---------------------------------------
