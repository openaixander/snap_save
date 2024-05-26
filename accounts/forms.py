from django import forms

from .models import Account


# this is the registrationForm for both the photographer and the client
class PhotoRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password',
                'class':'form-control',
                'required':'Please enter your password',
                # 'name':'password'
            }
        )
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Confirm Password',
                'class':'form-control',
                'required':'Please enter your password',
                # 'name':'confirm_password'
            }
        )
    )
    
    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'bank_number',
            'password',
            ]
        
    
    
    def __init__(self, *args, **kwargs):
        super(PhotoRegistrationForm, self).__init__(*args, **kwargs)
        
        # this here is the bootstrap classes given to each field
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['phone_number'].widget.attrs['type'] = 'tel'
        self.fields['bank_number'].widget.attrs['placeholder'] = 'Bank Account'
        self.fields['bank_number'].widget.attrs['type'] = 'number'
        # self.fields['bank_number'].widget.attrs['min'] = '0'
        # self.fields['bank_number'].widget.attrs['step'] = '1'
        
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
    def clean(self):
        cleaned_data = super(PhotoRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")
        

class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password',
                'class':'form-control',
                'required':'Please enter your password',
                # 'name':'password'
            }
        )
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Confirm Password',
                'class':'form-control',
                'required':'Please enter your password',
                # 'name':'confirm_password'
            }
        )
    )
    
    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
        ]
        
        
    def __init__(self, *args, **kwargs):
        super(ClientRegistrationForm, self).__init__(*args, **kwargs)
        
        # this here is the bootstrap classes given to each field
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['phone_number'].widget.attrs['type'] = 'tel'
        
        
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
    def clean(self):
        cleaned_data = super(ClientRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")
        
        
        