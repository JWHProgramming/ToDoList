from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

REGEX_EMAIL = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData["first_name"]) < 2:
            errors["err_f_name"] = "First name must be at least 2 characters long"
        if len(postData["last_name"]) < 2:
            errors["err_l_name"] = "Last name must be at least 2 characters long"
        if not REGEX_EMAIL.match(postData["email"]):
            errors["err_email"] = "Email must be in the correct format"
        matching_users = User.objects.filter(email=postData["email"].lower())
        if len(matching_users) > 0:
            errors["email_taken"] = "Email taken"
        if len(postData["password"]) < 6:
            errors["err_password"] = "Password must be at least 6 characters"
        if postData["password"] != postData["password_confirmation"]:
            errors["err_password_match"] = "Passwords do not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        matching_user = User.objects.filter(email=postData["login_email"].lower())

        if len(matching_user) < 1:
            errors["email_login_matcher"] = "Email does not exist"
        if len(matching_user) > 0:
            user = matching_user[0]
            if not bcrypt.checkpw(postData["login_password"].encode(), user.password.encode()):
                errors["password_error"] = "Information incorrect"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}

        if len(postData["title"]) < 1:
            errors["title_length"] = "Title must be at least 1 character long"
        return errors

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()