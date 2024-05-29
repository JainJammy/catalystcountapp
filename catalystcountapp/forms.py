from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django import forms
"""creating sign up form"""
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user
"""creating upload file form"""    
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select File')

"""creating add users form"""
class AddUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput, required=True)
        self.fields['confirm_password'] = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
