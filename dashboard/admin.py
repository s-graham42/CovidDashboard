from django.contrib import admin

# Register your models here.
from .models import CsvFile, State

admin.site.register(CsvFile)
admin.site.register(State)