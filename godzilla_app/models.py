from django.db import models

import bcrypt
import re

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address."
        else:
            user_list = User.objects.filter(email = post_data['email'])
            if len(user_list) > 0:
                errors['email'] = "Email is already in use."

        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if post_data['password'] != post_data['password_confirm']:
            errors['password_confirm'] = "Password entries must match."

        return errors


    def login_validator(self, post_data):
        errors = {}

        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid credentials."
        else:
            errors['email'] = "Invalid credentials."
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add  = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Message(models.Model):
    message_content = models.CharField(max_length = 255)
    movie = models.IntegerField()
    user = models.ForeignKey(User, related_name = 'messages', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add  = True)
    updated_at = models.DateTimeField(auto_now = True)


class Comment(models.Model):
    comment_content = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name = 'comments', on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name = 'comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add  = True)
    updated_at = models.DateTimeField(auto_now = True)
