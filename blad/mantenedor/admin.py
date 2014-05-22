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
    if not change:
      username = form.cleaned_data.get('username')
      user = AuthUser.objects.create_user(username=username, password=username)
      user.is_staff = user.is_active = True
      user.save()
      obj.user = user
      obj.save()

admin.site.register(Line, LineAdmin)
admin.site.register(AppUser, AppUserAdmin)
