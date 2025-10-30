from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
def is_password_strength(value):
    import re
    return len(value) > 8 or re.search(r"\d", value) or re.search(r"[A-Z]", value)
class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'tel', 'autocomplete': 'off'}),
        label='شماره همراه',required=True
    )
    password = forms.CharField(
        widget= forms.PasswordInput(attrs= {'autocomplete':'off'}),
        label='کلمه عبور',required=True
    )
    
User = get_user_model()
class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={}),
        label='نام',required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={}),
        label='نام خانوادگی',required=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'tel', 'autocomplete': 'off'}),
        label='شماره همراه',required=True
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={}),
        label='ایمیل (اختیاری)',required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
        label='رمز عبور',required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
        label='تکرار رمز عبور',required=True,
    )
    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password not in password2 :
            raise ValidationError({'password2' : 'مقادیر رمز عبور همخوانی ندارند !'})
        else :
            if not is_password_strength(password):
                raise ValidationError({'password': 'روز عبور حداقل باید 8 کاراکتر و شامل حروف انگلیسی کوچک و بزرگ و اعداد باشد !'})
            #validate_password(password)
        phone = self.cleaned_data.get('phone')
        if phone is None:
            raise ValidationError({'phone': 'شماره تلفن باید وارد شود !'})
        else :
            user = User.objects.filter(username=phone).first()
            if user is not None :
                raise ValidationError({'phone': 'کاربری با این شماره تلفن وارد شده است !'})
        email = self.cleaned_data.get('email')
        if email :
            user = User.objects.filter(email = email)
            if user is not None :
                raise ValidationError({'email': 'کاربری با این ایمیل در سیستم وجود دارد !'})
        return super().clean()