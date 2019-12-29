from django.db import models
from django.template.defaultfilters import slugify

class Restaurant (models.Model):
    name = models.CharField(max_length=120, unique=True, blank=False)
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']
