# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Messages(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    message_text = models.CharField(max_length=50000)
    sent_date = models.DateTimeField('dateSent')
