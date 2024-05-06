from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from .models import Customer, Address


class UserAddressForm(forms.ModelForm):
    """
    Form for user address information.
    """
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode", "country"]

    def __init__(self, *args, **kwargs):
        """
        Initialize form fields and attributes.
        """
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name*"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone (Optional)"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "House Number and Street*"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Second Address Line (Optional)"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "City, State*"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Post Code*"}
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Country*"}
        )

        # Set fields as not required
        self.fields["address_line2"].required = False
        self.fields["phone"].required = False


class UserLoginForm(AuthenticationForm):
    """
    Login form for users.
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    """
    Form for user registration.
    """
    name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name', 'email',)

    def clean_user_name(self):
        """
        Clean and validate username.
        """
        name = self.cleaned_data['name'].lower()
        r = Customer.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return name

    def clean_password2(self):
        """
        Clean and validate repeated password.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        """
        Clean and validate email.
        """
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        """
        Initialize form fields and attributes.
        """
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username*'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-Mail Address*', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password*'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password*'})


class PwdResetForm(PasswordResetForm):
    """
    Form for password reset.
    """
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'E-Mail Address', 'id': 'form-email'}))

    def clean_email(self):
        """
        Clean and validate email for password reset.
        """
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    """
    Form for resetting password.
    """
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):
    """
    Form for user profile editing.
    """
    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username'}))
    
    profile_image = forms.ImageField(label='Profile Image', required=False)

    class Meta:
        model = Customer
        fields = ('email', 'name', 'profile_image',)

    def __init__(self, *args, **kwargs):
        """
        Initialize form fields and attributes.
        """
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True