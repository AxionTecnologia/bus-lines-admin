#!/usr/bin/python
# -*- coding: utf-8 -*-

from itertools import repeat

from django.contrib import admin

from mantenedor.models import AppUser
from linea.models import Person, Bus, Route, Point, Itinerary
from linea.forms import BusModelForm, PersonModelForm, RouteModelForm, ItineraryModelForm

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

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    line = AppUser.objects.get(user=request.user).line
    for instance in instances:
      instance.line = line
      instance.save()

  def get_queryset(self, request):
    queryset = super(BaseModelAdmin, self).get_queryset(request)
    if not request.user.is_superuser:
      user = AppUser.objects.get(user=request.user)
      queryset = queryset.filter(line = user.line)
    return queryset

  def get_model_perms(self, request):
    """Every user that is not a superuser has perms"""
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


class BaseTabularInline(admin.TabularInline):

  exclude = ('line',)

  def has_add_permission(self, request):
    return True

  def has_change_permission(self, request, instance=None):
    return True


class PersonAdmin(BaseModelAdmin):
  list_display = ('get_full_name', 'get_line_number')
  form = PersonModelForm


class BusAdmin(BaseModelAdmin):
  form = BusModelForm


class PointInline(BaseTabularInline):
  model = Point
  extra = 1


class RouteAdmin(BaseModelAdmin):
  form = RouteModelForm
  inlines = (PointInline,)


class ItineraryAdmin(BaseModelAdmin):
  form = ItineraryModelForm

#class RecorridoAdmin(BaseModelAdmin):
#  form = RouteModelForm
#
#  def add_view(self, request):
#    return HttpResponseRedirect(reverse("admin:linea_route_changelist"))
#
#  def get_urls(self):
#    from django.conf.urls import patterns, url
#    urls = super(RecorridoAdmin, self).get_urls()
#    my_urls = patterns('',
#      url(r'^add/$', self.admin_site.admin_view(self.add_view),
#      name='admin_update_feeds'))
#    print my_urls + urls
#    return my_urls + urls

admin.site.register(Person, PersonAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Itinerary, ItineraryAdmin)
