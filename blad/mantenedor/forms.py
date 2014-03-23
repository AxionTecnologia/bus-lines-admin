#!/usr/bin/python
#-*- encoding: UTF-8 -*-

from django import forms
from mantenedor.models import Line, User

class UserModelForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super(UserModelForm,self).__init__(*args,**kwargs)
    if kwargs.get('instance'):
      self.initial["username"] = kwargs.get('instance').user.username

  line = forms.ModelChoiceField(queryset=Line.objects.all())
  username = forms.CharField(label="Nombre usuario")

  class Meta:
    model = User

