from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from users_app.models import CustomGroup


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Enter password'})


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Enter login'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Enter password'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Repeat password'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "First name",
            'last_name': "Last name",
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Enter last name'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class UpdateUserForm(forms.ModelForm):
    check_password = forms.CharField(label="Password",
                                     widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'Enter password to confirm'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'check_password']
        labels = {
            'email': 'E-mail',
            'first_name': "First name",
            'last_name': "Last name",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Enter login'}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Enter last name'}),
        }

    def clean_check_password(self):
        password = self.cleaned_data['check_password']
        if not password:
            raise forms.ValidationError("Enter password")
        if not self.instance.check_password(password):
            raise forms.ValidationError("Enter correct password")
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class PostGroupForm(forms.ModelForm):
    name = forms.CharField(max_length=255,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter name'}))
    admin = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Enter admin username'}))

    class Meta:
        model = CustomGroup
        exclude = ['admin']
        fields = ['name', 'description', 'admin']
        widgets = {
            'description': forms.Textarea(attrs={'style': "height: 140px",
                                                 'class': 'form-control',
                                                 'placeholder': 'Enter description'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        if 'instance' in kwargs:
            self.fields['name'].initial = self.instance.group.name
            self.fields['admin'].initial = self.instance.admin.username

    def clean_admin(self):
        adminname = self.cleaned_data['admin']
        try:
            admin = User.objects.get(username=adminname)
            return admin
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")


class AddUserToGroupForm(forms.Form):
    user = forms.CharField(label='Add user in the group',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter username'}))

    def __init__(self, group=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if group:
            self.group = group

    def clean_user(self):
        username = self.cleaned_data['user']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
        else:
            if user in self.group.user_set.all():
                raise forms.ValidationError("User is already in the group")
        return user
