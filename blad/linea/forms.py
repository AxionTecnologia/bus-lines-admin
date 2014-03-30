#!/usr/bin/python
#-*- encoding: UTF-8 -*-

from django import forms

from mantenedor.models import AppUser
from linea.models import Bus, Person, Route

class BaseModelForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    request = kwargs.pop('request', None)
    self.app_user = AppUser.objects.get(user=request.user)
    super(BaseModelForm, self).__init__(*args, **kwargs)


class BusModelForm(BaseModelForm):

  def clean(self):
    cleaned_data = self.cleaned_data
    if Bus.objects.filter(ppu=cleaned_data.get('ppu'), line=self.app_user.line).count() >= 1:
      raise forms.ValidationError("Bus already exists!")
    return cleaned_data

  class Meta:
    model = Bus


class PersonModelForm(BaseModelForm):
  class Meta:
    model = Person


class RouteModelForm(BaseModelForm):
  class Meta:
    model = Route
