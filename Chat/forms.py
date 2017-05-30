# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django import forms

class UserForms(forms.ModelForm):
    password =  forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']
