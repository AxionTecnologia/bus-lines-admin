#!/usr/bin/python
#-*- encoding: UTF-8 -*-

from django.utils.translation import ugettext as _
from django import forms

from mantenedor.models import Line, AppUser

class AppUserModelForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super(AppUserModelForm,self).__init__(*args,**kwargs)
    if kwargs.get('instance'):
      self.initial["username"] = kwargs.get('instance').user.username

  line = forms.ModelChoiceField(queryset=Line.objects.all())
  username = forms.CharField(label="Nombre usuario")

  def clean_username(self):
    username = self.cleaned_data['username']
    if AppUser.objects.filter(user__username=username).count() > 0:
      raise forms.ValidationError(_("User name already exists."))
    return username


  class Meta:
    model = AppUser
