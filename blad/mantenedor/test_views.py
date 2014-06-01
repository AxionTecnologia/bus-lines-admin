# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from mantenedor.models import AuthUser, Line, AppUser

class BaseViewTestCase(TestCase):

  def setUp(self):
    self.client = Client()
    user = AuthUser.objects.create_user(username="me", password="me")
    user.is_superuser = user.is_staff = user.is_active = True
    user.save()


class AdminMainViewTestCase(BaseViewTestCase):

  def test_superuser_can_only_have_access_to_mantenedor_and_auth(self):
    self.client.login(username="me", password="me")
    response = self.client.get(reverse("admin:index"))
    app_list = response.context['app_list']
    self.assertEqual(["Auth", "Mantenedor"], map(lambda app: app['name'], app_list))


class AppUserViewTestCase(BaseViewTestCase):

  def test_app_user_creation_add_auth_user_as_part_of_app_user(self):
    line = Line.objects.create(number=5)
    self.client.login(username="me", password="me")
    response = self.client.post(reverse("admin:mantenedor_appuser_add"), {'line': line.id, 'username': "minostro"})
    self.assertRedirects(response, reverse("admin:mantenedor_appuser_changelist"))
    self.assertEqual(1, AppUser.objects.all().count())
    self.assertEqual(1, AuthUser.objects.filter(username="minostro").count())


  def test_it_is_not_possible_to_create_two_repeated_users(self):
    line = Line.objects.create(number=5)
    self.client.login(username="me", password="me")

    response = self.client.post(reverse("admin:mantenedor_appuser_add"), {'line': line.id, 'username': "minostro"})
    self.assertRedirects(response, reverse("admin:mantenedor_appuser_changelist"))

    response = self.client.post(reverse("admin:mantenedor_appuser_add"), {'line': line.id, 'username': "minostro"})
    #NOTE: I couldn't use assertFormError(response, 'form'..), because AppUserForm is not in the context map.
    # It seems assertFormError was meant to work with personalized views and not with Django Admin views
    # response.context['adminform'].form.errors does the trick, but I prefered to use contains.
    self.assertContains(response, "User name already exists.", status_code=200)

    self.assertEqual(1, AppUser.objects.all().count())
    self.assertEqual(1, AuthUser.objects.filter(username="minostro").count())

  def test_display_username_when_modifying_an_app_user(self):
    line = Line.objects.create(number=5)
    app_user = AppUser.objects.create(line=line, user=AuthUser.objects.get(username="me"))
    self.client.login(username="me", password="me")
    response = self.client.get(reverse("admin:mantenedor_appuser_change", args=[app_user.id]))
    #NOTE: This is frustrating: there is no a clean way to check values
    # by using the form that is in context.  I have to use global search
    # on the response content :-(
    # It would be nice to have something like
    # assertFormFieldContent(response, 'adminform', 'username', 'me')
    self.assertContains(response, 'value="me"', status_code=200)
