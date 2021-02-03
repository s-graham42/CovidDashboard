from django.contrib import admin

# Register your models here.
from .models import CsvFile, State, Entry

admin.site.register(CsvFile)
admin.site.register(State)
admin.site.register(Entry)