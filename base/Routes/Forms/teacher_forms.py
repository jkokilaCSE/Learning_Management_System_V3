from django import forms
from django.contrib.auth.models import User
from base import models
from base.models import Department

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os


def validate_image_file(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Only image files (JPG, JPEG, PNG, GIF) are allowed.'))


class TeacherUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ['address', 'mobile', 'profile_pic', 'role', 'department']

    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('hod', 'Hod'),
        ('admin', 'Admin'),
    )
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(),
                                        empty_label='Select department',
                                        to_field_name='short_name',
                                        label='Department')
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), initial='admin', label='Role')

    profile_pic = forms.ImageField(validators=[validate_image_file], label='Profile Picture')

    

class TeacherFormhod(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ['address', 'mobile', 'profile_pic', 'role', 'department']

    ROLE_CHOICES = (
        ('staff', 'Staff'),
    )
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(),
                                        empty_label='Select department',
                                        to_field_name='short_name',
                                        label='Department')
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), initial='admin', label='Role')
    profile_pic = forms.ImageField(validators=[validate_image_file], label='Profile Picture')

class TeacherForm1(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ['address', 'mobile', 'profile_pic', 'role', 'department']

    ROLE_CHOICES = (
        ('admin', 'Admin'),
    )
    
    DEPARTMENT_CHOICES = (
        ('', 'Select department'),
        ('admin', 'Admin'),
    )
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES,
                                    label='Department')
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), initial='admin', label='Role')
    profile_pic = forms.ImageField(validators=[validate_image_file], label='Profile Picture')


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('name', 'description', 'short_name')
