from django import forms
from django.contrib.auth.models import User
from ... import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os


def validate_image_file(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Only image files (JPG, JPEG, PNG, GIF) are allowed.'))


class StudentUserForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class StudentForm(forms.ModelForm):

    joinned_year = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    role_no = forms.IntegerField()
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(),
                                        empty_label='Select department',
                                        to_field_name='short_name',
                                        label='Department')
    profile_pic = forms.ImageField(validators=[validate_image_file], label='Profile Picture')
    

    class Meta:
        model = models.Student
        fields = ['address', 'mobile', 'profile_pic',
                  'joinned_year', 'role_no', 'department','parent_mail_id','mail_id']
