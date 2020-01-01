from django.contrib import admin
from .models import Restaurant, Weekday, Schedule

class WeekdayAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Restaurant)
admin.site.register(Weekday, WeekdayAdmin)
admin.site.register(Schedule)
