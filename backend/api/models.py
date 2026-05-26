from django.contrib.gis.db import models


class Municipality(models.Model):
    name = models.CharField(max_length=255)
    geo = models.MultiPolygonField()
