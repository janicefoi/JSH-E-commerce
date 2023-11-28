from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="At least 8 characters",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text="Enter the same password",
    )

    class Meta:
        model = UserProfile
        fields = ("username", "email", "password1", "password2")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'location', 'phone_number']

    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'type': 'tel'}))  # Phone number input type "tel"

class UserEmailUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']
