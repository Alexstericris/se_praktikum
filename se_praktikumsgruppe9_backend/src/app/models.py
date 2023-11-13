from django.db import models

"""
    Bitte zugehörige Dokumentation beachten!

    Wir nehmen an, dass User nicht gelöscht werden können (um Logs konsistent zu halten), weswegen wir überall wo ein User ein Foreign Key ist on_delete auf PROTECT setzten.
    Dahingegen sollten wenn Metadaten gelöscht werden auch die dazugehörigen Daten gelöscht werden.
    Werden Raw Meta Data Einträge gelöscht, wird bei allen filtered Meta Data Einträgen zu diesem Eintrag die raw id auf null gesetzt, damit Data Owner nicht durch das Löschen ihrer Daten FilteredData löschen können.

"""

class Log(models.Model):
    # id existiert implizit als primary key!
    initiator = models.ForeignKey('user.User', on_delete=models.PROTECT, null=False)
    recorded_time = models.DateTimeField(null=True)
    action = models.TextField()

    def __str__(self):
        return str(self.initiator) + " " + str(self.recorded_time)


class MetaData(models.Model):
    # id existiert implizit als primary key!
    name = models.CharField("Name", unique=True, null=True, max_length=240)
    time_recorded = models.DateTimeField(null=False)
    creator = models.ForeignKey('user.User', on_delete=models.PROTECT,null=True)
    base = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Column(models.Model):
    # id existiert implizit als primary key!
    name = models.CharField("Name", null=False, max_length=240)
    unit = models.CharField("unit", null=True, max_length=240) # null=False
    value_data_type = models.CharField("datatype", null=False, max_length=240)
    applied_filters = models.CharField("applied_filters", null=False, max_length=240)
    meta_data = models.ForeignKey(MetaData, on_delete=models.CASCADE)


class DataTupel(models.Model):
    # id existiert implizit als primary key!
    relative_time = models.FloatField(null=False)
    bool_value = models.BooleanField(null=True)
    float_value = models.FloatField(null=True)
    string_value = models.CharField(null=True, max_length=240)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
