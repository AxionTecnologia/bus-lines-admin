#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from mantenedor.models import Line

class BaseModel(models.Model):
  line = models.ForeignKey(Line, blank=True, null=False)

  class Meta:
    abstract = True

class Bus(BaseModel):
  ppu = models.CharField(max_length=100)
  motor_number = models.CharField(max_length=100)
  chassis_number = models.CharField(max_length=100)
  serie_number = models.CharField(max_length=100)
  vin_number = models.CharField(max_length=100)
  manufacture_year = models.DateField()
  acquisition_date = models.DateField()
  inscription_date = models.DateField()

class Person(BaseModel):
  name = models.CharField(max_length=100)

  def get_line_number(self):
    return u"{0}".format(self.line.number)
  get_line_number.short_description = u"línea"

  def get_full_name(self):
    return u"{0}".format(self.name)
  get_full_name.short_description = u"nombre"
