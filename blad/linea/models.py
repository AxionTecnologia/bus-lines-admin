#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from mantenedor.models import Line

class BaseModel(models.Model):
  line = models.ForeignKey(Line, blank=True, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

class Person(BaseModel):
  DRIVER_LICENSE_TYPE_CHOICES = (
    ('A1', 'A1'),
  )

  id_number = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  surname = models.CharField(max_length=100)
  address = models.CharField(max_length=150)
  phone_number =  models.CharField(max_length=40)
  internal_identifier = models.CharField(max_length=100)
  is_owner = models.BooleanField()
  is_driver = models.BooleanField()
  driver_license_expires_at = models.DateField()
  driver_license_type = models.CharField(max_length=2, choices=DRIVER_LICENSE_TYPE_CHOICES)

  def get_line_number(self):
    return u"{0}".format(self.line.number)
  get_line_number.short_description = u"línea"

  def get_full_name(self):
    return u"{0}".format(self.name)
  get_full_name.short_description = u"nombre"


class Bus(BaseModel):
  ppu = models.CharField(max_length=100)
  motor_number = models.CharField(max_length=100)
  chassis_number = models.CharField(max_length=100)
  serie_number = models.CharField(max_length=100)
  vin_number = models.CharField(max_length=100)
  manufacture_year = models.IntegerField()
  acquisition_date = models.DateField()
  inscription_date = models.DateField()
  internal_identifier = models.CharField(max_length=100)
  bus_check_up_expires_at = models.DateField()
  belongs_to = models.ForeignKey(Person, related_name="belongs_to")
  driven_by = models.ForeignKey(Person, related_name="driven_by")


class Route(BaseModel):
  name = models.CharField(max_length=100)


class Point(BaseModel):
  route = models.ForeignKey(Route)
  x = models.DecimalField(max_digits=10, decimal_places=4)
  y = models.DecimalField(max_digits=10, decimal_places=4)
  radius = models.IntegerField()
  name = models.CharField(max_length=100)

  def __unicode__(self):
    return u"{0}".format(self.name)

class Itinerary(BaseModel):
  route = models.ForeignKey(Route)
  name = models.CharField(max_length=100)


class Checkpoint(BaseModel):
  point = models.ForeignKey(Point)
  itinerary = models.ForeignKey(Itinerary)
  duration = models.IntegerField(null=True, blank=False)
  tolerance = models.IntegerField(null=True, blank=False)
  fine = models.IntegerField(null=True, blank=False)


class Schedule(BaseModel):
  DAYS_OF_THE_WEEK_CHOICES = (
    ('monday', 'Monday'),
    ('tuesday','Tuesday'),
    ('wednesday','Wednesday'),
    ('thursday','Thursday'),
    ('friday','Friday'),
    ('saturday','Saturday'),
    ('sunday','Sunday'),
  )

  itinerary = models.ForeignKey(Itinerary)
  day_of_the_week = models.CharField(max_length=10, choices=DAYS_OF_THE_WEEK_CHOICES)
  time_from = models.TimeField()
  time_to = models.TimeField()
