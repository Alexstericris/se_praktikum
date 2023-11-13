from django.db import models

from user.models import User

from app.models import MetaData

from app.models import Column


# Create your models here.
class Chart(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    metaData = models.ForeignKey(MetaData, on_delete=models.PROTECT, null=False)
    column = models.ForeignKey(Column, on_delete=models.PROTECT, null=False)
    chartType = models.CharField("chart_type", max_length=240)
