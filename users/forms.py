from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
import datetime
from django.conf import settings



BIRTH_YEAR_CHOICES = [x for x in range(1920, 2019)]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'), input_formats=['%d-%m-%Y'], required=False)
    class Meta:
        model = Profile
        fields = ['image', 'date_of_birth', 'bio']

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        now = datetime.date.today()
        if dob and now < dob:
            raise forms.ValidationError("You cannot have that value for Date of Birth!")
