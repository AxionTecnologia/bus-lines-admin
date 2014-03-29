from django.contrib import admin
from mantenedor.models import Line, AppUser, AuthUser
from mantenedor.forms import AppUserModelForm

from django.contrib import auth

class LineAdmin(admin.ModelAdmin):
  pass

class AppUserAdmin(admin.ModelAdmin):
  form = AppUserModelForm
  list_display = ('get_username', 'get_line_number', 'is_active')
  exclude = ('user',)

  def save_model(self, request, obj, form, change):
    username = form.cleaned_data.get('username')
    user = AuthUser.objects.create_user(
      username=username,
      password=username)
    user.is_staff = True
    user.is_active = True
    user.save()
    obj.user = user
    obj.save()

class BusDriverAdmin(admin.ModelAdmin):
  exclude = ('created_by',)
  list_display = ('get_full_name', 'get_line_number')

  def save_model(self, request, obj, form, change):
    user = User.objects.get(user=request.user)
    obj.created_by = user
    obj.save()

  def get_queryset(self, request):
    queryset = super(BusDriverAdmin, self).get_queryset(request)
    if not request.user.is_superuser:
      user = User.objects.get(user=request.user)
      queryset = queryset.filter(created_by__line = user.line)
    return queryset

admin.site.register(Line, LineAdmin)
admin.site.register(AppUser, AppUserAdmin)
