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
2. Регистрируем приложение в Yndex для работы с сервисом
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
                Permission name # поле для выбора по каким полям проходит регисрация
                Access to email address # у нас заявлено что по emaill
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
    Client id: ID с страницы приложения Yndex. Поле: "ClientID"
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

---------------------------------------