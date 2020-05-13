from django import forms
from django.contrib.auth.forms import UserCreationForm
from UserCust.models import CustomUser

class RegForm(UserCreationForm):
    username = forms.CharField(label='', help_text='',
                        widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    lastname = forms.CharField(label='', help_text='',
                        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    password1 = forms.CharField(label='', help_text='',
                        widget=forms.TextInput(attrs={
                            'placeholder': 'Password',
                            'type': 'password', }))
    password2 = forms.CharField(label='', help_text='',
                        widget=forms.TextInput(attrs={
                            'placeholder': 'Confirm Password',
                            'type': 'password',}))
    email = forms.EmailField(max_length=200, help_text='', label='',
                        widget=forms.TextInput(attrs={
                            'placeholder': 'Email',
                            'type': 'email', }))
    agree = forms.BooleanField(required=True, label='',help_text="i'd like to receive PlacePass news and offers By signing up, I agree to the PlacePass Terms of Service and Privacy Policy.")

    def save(self, commit=True):
        user=super(RegForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['lastname']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    class Meta:
        model = CustomUser
        fields = ('username', 'lastname','email', 'password1', 'password2')
