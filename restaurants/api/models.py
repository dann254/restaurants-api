from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils import timezone

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
        now = timezone.localtime()
        current_time = now.time()
        today = now.isoweekday()
        schedule = self.schedules.filter(weekday__iso_weekday = today).first()
        midnight = datetime.strptime('00:00:00', '%H:%M:%S').time()

        if schedule is None:
            return False

        if schedule.opening_time < schedule.closing_time:
            if current_time >= schedule.opening_time and current_time < schedule.closing_time:
                return True

        elif schedule.add_overflow:
            if current_time >= midnight and current_time <= schedule.add_overflow:
                return True

        else:
            if current_time >= schedule.opening_time and current_time < midnight:
                return True
        return False

    @property
    def review_count(self):
        reviews = self.reviews.all()
        return len(reviews)

    @property
    def rating_average(self):
        reviews = self.reviews.all()
        rating = 0
        for review in reviews:
            rating += review.rating
        if rating != 0:
            return round(rating/len(reviews), 1)
        return 0.0

    def tomorrow(self, today):
        return self.schedules.filter(weekday__iso_weekday = today+1).first()


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
    add_overflow = models.TimeField(null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, related_name='schedules', on_delete=models.CASCADE)
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['restaurant', 'weekday']
        ordering = ['weekday__iso_weekday']

class Review(models.Model):
    rating = models.FloatField(unique=False, blank=False, null=False)
    review = models.TextField(unique=False, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
