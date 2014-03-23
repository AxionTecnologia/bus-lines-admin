#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Line(models.Model):
  number = models.IntegerField()

  def __unicode__(self):
    return u"Línea {0}".format(self.number)

class User(models.Model):
  user = models.ForeignKey(User, unique=True, blank=True, null=False)
  line = models.ForeignKey(Line)

  def __unicode__(self):
    return u"{0}".format(self.user.username)

  def get_username(self):
    return u"{0}".format(self.user.username)
  get_username.short_description = u"nombre de usuario"

  def get_line_number(self):
    return u"{0}".format(self.line.number)
  get_line_number.short_description = u"línea"

  def is_active(self):
    return self.user.is_active
  is_active.boolean = True
  is_active.short_description = u"¿Activo?"

class BusDriver(models.Model):
  name = models.CharField(max_length=100)
  created_by = models.ForeignKey(User, blank=True, null=False)

  def get_line_number(self):
    line = self.created_by.line
    return u"{0}".format(line.number)
  get_line_number.short_description = u"línea"

  def get_full_name(self):
    return u"{0}".format(self.name)
  get_full_name.short_description = u"nombre"