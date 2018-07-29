from django.contrib import admin
from . import models

admin.site.register(models.AuthToken)
admin.site.register(models.Article)
