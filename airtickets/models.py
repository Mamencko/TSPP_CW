from django.db import models


class Airport(models.Model):
    city = models.CharField('Місто', max_length=50)
    code = models.CharField('Код', max_length=10)
    country = models.CharField('Країна', max_length=50)
    name = models.CharField('Назва', max_length=50)

    def __str__(self):
        return self.city + ' ' + self.name + ' (' + self.code + ')'

    class Meta:
        verbose_name = 'Аеропорт'
        verbose_name_plural = 'Аеропорти'


class Ticket(models.Model):
    agency = models.CharField('Агенство', max_length=50)
    company = models.CharField('Авіакомпанія', max_length=100)
    departurePoint = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_point')
    departureTime = models.DateTimeField('Час відправлення')
    destinationPoint = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_point')
    destinationTime = models.DateTimeField('Час прибуття')
    price = models.PositiveIntegerField('Ціна')
    url = models.URLField('Посилання на купівлю')

    class Meta:
        verbose_name = 'Квиток'
        verbose_name_plural = 'Квитки'

    def __str__(self):
        return self.company + ' ' + self.agency

    def get_duration(self):
        duration = self.destinationTime - self.departureTime
        return duration
