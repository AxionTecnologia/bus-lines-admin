#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser

class AuthUser(AbstractUser):

  def has_module_perms(self, app_label):
    """Any user has module perms.
       This allows users(super or not) to see any app without creating
       specific permissions.
    """
    return True

  class Meta(AbstractUser.Meta):
    swappable = 'AUTH_USER_MODEL'


class Line(models.Model):
  number = models.IntegerField()

  def __unicode__(self):
    return u"Línea {0}".format(self.number)


class AppUser(models.Model):
  user = models.ForeignKey(AuthUser, unique=True, blank=True, null=False)
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
