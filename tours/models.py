import numpy

from django.db import models
from django.db.models import Min


class Facilities(models.Model):
    category = models.CharField('Категорія', max_length=50)
    name = models.CharField('Назва зручності', max_length=50)

    class Meta:
        verbose_name = 'Зручність'
        verbose_name_plural = 'Зручності'

    def __str__(self):
        return self.name


class Tour(models.Model):
    hotel = models.CharField('Готель', max_length=50)
    country = models.CharField('Країна', max_length=50)
    city = models.CharField('Місто', max_length=50)
    stars = models.PositiveSmallIntegerField('Зірки')
    image = models.ImageField('Зображення', upload_to='tours/')
    facilities = models.ManyToManyField(Facilities)

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Тури'

    def __str__(self):
        return self.hotel

    def get_rate(self):
        rates = self.review_set.values_list('rating', flat=True)
        return round(numpy.mean(rates), 1)

    def get_lowest_price(self):
        price = self.price_set.order_by('price').first()
        return price


class Price(models.Model):
    price = models.PositiveIntegerField('Ціна')
    nights = models.PositiveSmallIntegerField('Кількість ночей')
    meals = models.CharField('Харчування', max_length=50)
    date = models.DateField('Дата вильоту')
    agency = models.CharField('Турагенство', max_length=50)
    url = models.URLField('Посиляння на бронювання')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ціна'
        verbose_name_plural = 'Ціни'
        ordering = ['price']

    def __str__(self):
        return self.tour.hotel + ': ' + self.agency + ', ' + self.nights.__str__() + ' ночей'


class Review(models.Model):
    author = models.CharField('Автор', max_length=50)
    email = models.EmailField('Email')
    rating = models.FloatField('Рейтинг')
    text = models.TextField('Текст відгуку')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']

    def __str__(self):
        return self.author
