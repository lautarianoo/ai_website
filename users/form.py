from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя не существует')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль неправильный')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный пользователь отключён')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(label='Username', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Repeat', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'name', )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

class UserUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Username', max_length=80, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    send_email = forms.BooleanField(label=' Send Email', widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = User
        fields = ('name', 'send_email', )