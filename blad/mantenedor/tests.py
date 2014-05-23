# -*- coding: utf-8 -*-
from django.test import TestCase, Client

from mantenedor.models import AuthUser, Line, AppUser


class AuthUserTestCase(TestCase):

  def setUp(self):
    AuthUser.objects.create(username="superuser",
                            is_staff=True,
                            is_superuser=True)
    AuthUser.objects.create(username="not-superuser",
                            is_staff=True,
                            is_superuser=False)

  def test_not_superuser_has_module_perms(self):
    not_superuser = AuthUser.objects.get(username="not-superuser")
    self.assertEqual(True, not_superuser.has_module_perms("my_testing_app"))

  def test_superuser_has_not_module_perms(self):
    superuser = AuthUser.objects.get(username="superuser")
    self.assertEqual(True, superuser.has_module_perms("my_testing_app"))


class AppUserTestCase(TestCase):

  def setUp(self):
    active_auth = AuthUser.objects.create(username="me", is_active=True)
    not_active_auth = AuthUser.objects.create(username="you", is_active=False)
    line = Line.objects.create(number=5)
    AppUser.objects.create(user=active_auth, line=line)
    AppUser.objects.create(user=not_active_auth, line=line)

  def test_unicode(self):
    user = AppUser.objects.get(user=AuthUser.objects.get(username="me"))
    self.assertEqual("me", user.__unicode__())

  def test_get_username(self):
    user = AppUser.objects.get(user=AuthUser.objects.get(username="me"))
    self.assertEqual("me", user.get_username())

  def test_get_line_number(self):
    user = AppUser.objects.get(user=AuthUser.objects.get(username="me"))
    self.assertEqual("5", user.get_line_number())

  def test_active_user_is_active(self):
    user = AppUser.objects.get(user=AuthUser.objects.get(username="me"))
    self.assertEqual(True, user.is_active())

  def test_not_active_user_is_not_active(self):
    user = AppUser.objects.get(user=AuthUser.objects.get(username="you"))
    self.assertEqual(False, user.is_active())


class LineTestCase(TestCase):

  def setUp(self):
    Line.objects.create(number=6)

  def test_unicode(self):
    line = Line.objects.get(number=6)
    self.assertEqual(u"Línea 6", line.__unicode__())


class AdminMainPageTestCase(TestCase):

  def setUp(self):
    user = AuthUser.objects.create_user(username="me", password="me")
    user.is_superuser = user.is_staff = user.is_active = True
    user.save()

  def test_superuser_can_only_have_access_to_mantenedor_and_auth(self):
    client = Client()
    client.login(username="me", password="me")
    response = client.get("/admin/")
    app_list = response.context['app_list']
    self.assertEqual(["Auth", "Mantenedor"], map(lambda app: app['name'], app_list))

