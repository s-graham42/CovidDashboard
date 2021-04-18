from django.db import models

# DB Model to hold uploaded csv files.
class CsvFile(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description  = models.TextField()
    file = models.FileField(upload_to='uploaded_csv_files')
    # access file details: (CsvFile object).file.name  / (CsvFile object).file.url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class State(models.Model):
    name = models.CharField(max_length=150)
    abbreviation = models.CharField(max_length=2)
    fips = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #entries = List of entries for this state.

class Entry(models.Model):
    date = models.DateField()
    cases_c = models.IntegerField() # cumulative cases
    cases_d = models.IntegerField() # daily cases
    deaths_c = models.IntegerField() # cumulative deaths
    deaths_d = models.IntegerField() # daily deaths
    state = models.ForeignKey(State, related_name="entries", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
