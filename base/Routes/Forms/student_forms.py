from django import forms
from django.contrib.auth.models import User
from ... import models
from base.models import Student

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

from django import forms
from django.core.validators import RegexValidator
from base.models import Student, Department
from django.core.validators import RegexValidator, validate_email

class StudentForm(forms.ModelForm):

    joinned_year = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    role_no = forms.IntegerField()

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label='Select department',
        to_field_name='short_name',
        label='Department'
    )

    profile_pic = forms.ImageField(
        validators=[validate_image_file],
        label='Profile Picture',
        required=False
    )

    # Regular expression to validate the mobile field (only numeric values allowed)
    numeric_validator = RegexValidator(
        regex=r'^[0-9]+$',
        message='Mobile number must contain only numeric digits.'
    )

    mobile = forms.IntegerField(validators=[numeric_validator])
    parent_mail_id = forms.EmailField(validators=[validate_email])
    mail_id = forms.EmailField(validators=[validate_email])

    class Meta:
        model = Student
        fields = ['address', 'mobile', 'profile_pic', 'joinned_year', 'role_no', 'department', 'parent_mail_id', 'mail_id']

    def clean(self):
        cleaned_data = super().clean()
        parent_mail_id = cleaned_data.get("parent_mail_id")
        mail_id = cleaned_data.get("mail_id")

        # Check if the parent_mail_id and mail_id are unique
        if Student.objects.filter(parent_mail_id=parent_mail_id).exists():
            raise forms.ValidationError("Parent email already exists.")
        if Student.objects.filter(mail_id=mail_id).exists():
            raise forms.ValidationError("Email already exists.")

        return cleaned_data