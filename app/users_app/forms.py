from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .models import CustomGroup

UserModel = get_user_model()


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Enter password'})


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Enter username'}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter email address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Enter last name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Repeat password'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class UpdateUserForm(forms.ModelForm):
    check_password = forms.CharField(label='Enter password to identify',
                                     widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'Enter password to confirm'}))

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name']
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
        if not self.instance.check_password(password):
            raise forms.ValidationError("Enter correct password")
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserModel.objects.filter(email=email).exclude(pk=self.instance.pk)
        if email and user.exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Enter the old password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'Enter a new password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'Repeat a new password'})


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': 'formal_placeholder'})


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': 'formal_placeholder'})


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
            admin = UserModel.objects.get(username=adminname)
            return admin
        except UserModel.DoesNotExist:
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
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
        else:
            if user in self.group.user_set.all():
                raise forms.ValidationError("User is already in the group")
        return user
