from django import forms
from django.forms import ModelForm
from .models import Account
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='email address')
    password = forms.CharField(label='password', widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = [ 'email', 'password']

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
        
class LoginForm(forms.Form): # 以下追記箇所
    email = forms.EmailField(label='email address')
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    
class UserChangeForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email']

    def __init__(self, email=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if email:
            self.fields['email'].widget.attrs['value'] = email
    def update(self, user):
        user.email = self.cleaned_data['email']
        user.save()
        


class MyPasswordChangeForm(PasswordChangeForm):

    # テンプレートにおいて表示されるinputタグのカスタマイズは以下のように行う（下は一例）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'Account'# classの指定
        self.fields['new_password1'].widget.attrs['class'] = 'Account'
        self.fields['new_password2'].widget.attrs['class'] = 'Account'
        self.fields['new_password1'].widget.attrs['placeholder'] = '半角英数字８文字以上'# placeholderの指定
        self.fields['new_password2'].widget.attrs['placeholder'] = 'パスワード確認用'
