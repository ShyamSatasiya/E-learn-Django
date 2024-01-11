from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import *


class Course_Detail_Form(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add the 'form-control' class to each field's widget
            field.widget.attrs['class'] = 'form-control'
            # Optionally, you can also add a placeholder attribute
            field.widget.attrs['placeholder'] = f'Enter {field_name}'