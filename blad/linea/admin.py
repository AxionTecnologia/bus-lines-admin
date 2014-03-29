#!/usr/bin/python
# -*- coding: utf-8 -*-

from itertools import repeat

from django.contrib import admin

from mantenedor.models import AppUser
from linea.models import Person, Bus
from linea.forms import BusModelForm

from django.contrib import auth

class BaseModelAdmin(admin.ModelAdmin):
  """This base model admin is intended to scope
     every object, created inside the Line app, by user.
     In this way we can use the same django app for multiple lines
     displaying the proper info.
  """

  exclude = ('line',)

  def save_model(self, request, obj, form, change):
    user = AppUser.objects.get(user=request.user)
    obj.line = user.line
    obj.save()

  def get_queryset(self, request):
    queryset = super(BaseModelAdmin, self).get_queryset(request)
    if not request.user.is_superuser:
      user = AppUser.objects.get(user=request.user)
      queryset = queryset.filter(line = user.line)
    return queryset

  def get_model_perms(self, request):
    """Every user that is not superuser has perms"""
    mappings = super(BaseModelAdmin, self).get_model_perms(request).keys()
    mapping_value = True
    if request.user.is_superuser:
      mapping_value = False
    return dict(zip(mappings,repeat(mapping_value, len(mappings))))

  def has_add_permission(self, request):
    return True

  def has_change_permission(self, request, object=None):
    return True

  def get_form(self, request, obj=None, **kwargs):
    ModelForm = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
    class ModelFormMetaClass(ModelForm):
      def __new__(cls, *args, **kwargs):
        kwargs['request'] = request
        return ModelForm(*args, **kwargs)
    return ModelFormMetaClass


class PersonAdmin(BaseModelAdmin):
  list_display = ('get_full_name', 'get_line_number')

class BusAdmin(BaseModelAdmin):
  form = BusModelForm

admin.site.register(Person, PersonAdmin)
admin.site.register(Bus, BusAdmin)
