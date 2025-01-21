from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(forms.ModelForm):
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your address (optional)',
            'id': 'address-input'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your phone number (optional)',
            'id': 'phone-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter a strong password',
            'id': 'password-input'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'address', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your username',
                'id': 'username-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email',
                'id': 'email-input'
            }),
        }

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'address': self.cleaned_data.get('address'),
                    'phone_number': self.cleaned_data.get('phone_number')
                }
            )
        return user
# Profile form to update user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone_number']

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full Name")
    address = forms.CharField(widget=forms.Textarea, label="Shipping Address")
    city = forms.CharField(max_length=100, label="City")
    state = forms.CharField(max_length=100, label="State")
    postal_code = forms.CharField(max_length=20, label="Postal Code")
    phone = forms.CharField(max_length=20, label="Phone Number")
    email = forms.EmailField(label="Email Address")
