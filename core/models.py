from abc import abstractclassmethod
from django.db import models
from . import managers


class AbstractTimeStamped(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True  # 데이터베이스에 등록 안됨
