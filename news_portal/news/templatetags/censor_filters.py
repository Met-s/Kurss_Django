from django import template

register = template.Library()

CENSOR_LIST = ['сколько', 'пиво', 'Сколько', 'Пиво',
               'плавание', 'корабли', 'Плавание', 'Корабли',
               'укрепления', 'развития', 'Укрепления', 'Развития',
               'немецкого', 'сумели', 'Немецкого', 'Сумели',
               ]


@register.filter()
def censor(value):
    for i in CENSOR_LIST:
        value = value.replace(i, "*" * len(i))
    return f'{value}'
