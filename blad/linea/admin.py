from django.contrib import admin
from linea.models import Person, Bus
from linea.forms import BaseModelForm

from django.contrib import auth

class BaseModelAdmin(admin.ModelAdmin):
  """This base model admin is intended to scope
     every object, created inside the Line app, by user.
     In this way we can use the same django app for multiple lines
     displaying the proper info.
  """

  def save_model(self, request, obj, form, change):
    super(BaseModelAdmin, self).save_model(self, request, obj, form, change)
    user = User.objects.get(user=request.user)
    obj.line = user.line
    obj.save()

  def get_queryset(self, request):
    queryset = super(BaseModelAdmin, self).get_queryset(request)
    if not request.user.is_superuser:
      user = User.objects.get(user=request.user)
      queryset = queryset.filter(line = user.line)
    return queryset

  def get_model_perms(self, request):
    return {} if request.user.is_superuser else  super(BaseModelAdmin, self).get_model_perms(request)


class PersonAdmin(BaseModelAdmin):
  exclude = ('created_by',)
  list_display = ('get_full_name', 'get_line_number')

class BusAdmin(BaseModelAdmin):
  form = BaseModelForm
  pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Bus, BusAdmin)
