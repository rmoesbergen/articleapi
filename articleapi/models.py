#!/usr/bin/env python3

from django.db import models
from django.contrib.auth.models import User


class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=32, db_index=True)
    expires = models.DateTimeField()


class Article(models.Model):
    subject = models.CharField(max_length=1024)
    body = models.TextField(max_length=64000)
    author = models.CharField(max_length=255)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return "{0} ({1})".format(self.subject, self.pk)
