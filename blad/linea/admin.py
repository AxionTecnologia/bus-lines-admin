#!/usr/bin/python
# -*- coding: utf-8 -*-

from itertools import repeat

from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote

from mantenedor.models import AppUser
from linea.models import Person, Bus, Route, Point, Itinerary, Checkpoint, Schedule
from linea.forms import BusModelForm, PersonModelForm, RouteModelForm, ItineraryModelForm, ScheduleModelForm

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
    """Passing request to ModelForms to perfom some user based checkings"""
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


class CheckpointInline(BaseTabularInline):
  model = Checkpoint
  extra = 1


class ItineraryAdmin(BaseModelAdmin):
  form = ItineraryModelForm
  inlines  = (CheckpointInline,)

  def get_formsets(self, request, obj=None):
    return [] if obj is None else super(ItineraryAdmin, self).get_formsets(request, obj)

  def change_view(self, request, object_id, form_url='', extra_context=None):
    obj = self.get_object(request, unquote(object_id))
    if Checkpoint.objects.filter(itinerary=obj).count() == 0:
      for point in Point.objects.filter(route=obj.route):
        checkpoint = Checkpoint(point=point, itinerary=obj, line=obj.line)
        checkpoint.save()
    inline_instance = CheckpointInline(self.model, self.admin_site)
    inline_instance.max_num = 0
    Formset = inline_instance.get_formset(request, obj)
    formset = Formset(instance=obj, prefix=Formset.get_default_prefix())
    fieldsets = list(inline_instance.get_fieldsets(request, obj))
    readonly = list(inline_instance.get_readonly_fields(request, obj))
    prepopulated = dict(inline_instance.get_prepopulated_fields(request, obj))
    inline_admin_formsets = helpers.InlineAdminFormSet(inline_instance, formset, fieldsets, prepopulated, readonly, model_admin=self)
    extra_context = {'inline_admin_formsets': [inline_admin_formsets]}
    return super(ItineraryAdmin, self).change_view(request, object_id, form_url, extra_context)


class ScheduleAdmin(BaseModelAdmin):
  form = ScheduleModelForm


admin.site.register(Person, PersonAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(Schedule, ScheduleAdmin)
