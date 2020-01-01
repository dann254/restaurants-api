from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime

class Restaurant(models.Model):
    name = models.CharField(max_length=120, unique=True, blank=False)
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Restaurant, self).save(*args, **kwargs)

    @property
    def open(self):
        now = datetime.utcnow()
        current_time = now.time()
        today = now.isoweekday()
        schedule = self.schedules.filter(weekday__iso_weekday = today).first()

        if current_time >= schedule.opening_time and current_time <= schedule.closing_time:
            return True
        return False

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created']


class Weekday(models.Model):
    day = models.CharField(max_length=10, unique=True, blank=False)
    iso_weekday = models.PositiveIntegerField()

    def __str__(self):
        return self.day


class Schedule(models.Model):
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    restaurant = models.ForeignKey(Restaurant, related_name='schedules', on_delete=models.CASCADE)
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['restaurant', 'weekday']
        ordering = ['weekday__iso_weekday']
