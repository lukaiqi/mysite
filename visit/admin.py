from django.contrib import admin
from .models import IpNumber, DayNumber, VisitNumber


# Register your models here.
@admin.register(IpNumber)
class IpNumberAdmin(admin.ModelAdmin):
    list_display = ('ip', 'count')


@admin.register(VisitNumber)
class VisitNumberAdmin(admin.ModelAdmin):
    list_display = ('site', 'count')


@admin.register(DayNumber)
class DayNumberAdmin(admin.ModelAdmin):
    list_display = ('day', 'count')
