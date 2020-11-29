import numpy
from django.db import models


class HotelFacilities(models.Model):
    category = models.CharField('Категорія', max_length=50)
    name = models.CharField('Назва зручності', max_length=50)

    class Meta:
        verbose_name = 'Зручність'
        verbose_name_plural = 'Зручності'

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField('Назва готелю', max_length=50)
    description = models.TextField('Опис')
    country = models.CharField('Країна', max_length=50)
    city = models.CharField('Місто', max_length=50)
    street = models.CharField('Вулиця', max_length=50)
    stars = models.PositiveSmallIntegerField('Зірки')
    facilities = models.ManyToManyField(HotelFacilities)
    url = models.URLField('Посилання на бронь')

    class Meta:
        verbose_name = 'Готель'
        verbose_name_plural = 'Готелі'

    def __str__(self):
        return self.name

    def get_rate(self):
        rates = self.hotelreview_set.values_list('rating', flat=True)
        return round(numpy.mean(rates), 1)

    def get_lowest_price_room(self):
        room = self.room_set.order_by('price').first()
        return room


class HotelImages(models.Model):
    image = models.ImageField('Зображення', upload_to='hotels/')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Зображення готелю'
        verbose_name_plural = 'Зображення готелів'

    def __str__(self):
        return self.hotel.name + ': ' + self.image.__str__()


class Room(models.Model):
    type = models.CharField('Тип кімнати', max_length=50)
    description = models.TextField('Опис кімнати')
    capacity = models.PositiveSmallIntegerField('Місткість кімнати')
    price = models.PositiveSmallIntegerField('Вартість кімнати')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кімната готелю'
        verbose_name_plural = 'Кімнати готелів'

    def __str__(self):
        return self.type


class PlacesNearHotel(models.Model):
    place = models.CharField('Мічце', max_length=100)
    distance = models.FloatField('Відстань від готелю')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Місце поруч з готелем'
        verbose_name_plural = 'Місця поруч з готелемя'

    def __str__(self):
        return self.place


class HotelReview(models.Model):
    author = models.CharField('Автор', max_length=50)
    email = models.EmailField('Email')
    rating = models.FloatField('Рейтинг')
    text = models.TextField('Текст відгуку')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']

    def __str__(self):
        return self.author
