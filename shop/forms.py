from django import forms
from .models import User,Book,Category

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({"class":"form-control","placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput({"class":"form-control","placeholder":"Password"}))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput({"class":"form-control","placeholder":"username"}))
    phone_number = forms.CharField(widget=forms.TextInput({"class":"form-control","placeholder":"Phone"}))
    first_name = forms.CharField(widget=forms.TextInput({"class":"form-control","placeholder":"First name"}))
    last_name = forms.CharField(widget=forms.TextInput({"class":"form-control","placeholder":"Last name"}))

    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput({"class": "form-control", "placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ('username','phone_number','first_name','last_name','password','confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password !=confirm_password:
            raise forms.ValidationError("Password do not match")
        return password

class CreateBookForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput({"class":"form-control","placeholder":"nomi"}))
    description = forms.CharField(widget=forms.Textarea({"class":"form-control","placeholder":"Matni"}))
    image = forms.ImageField(widget=forms.FileInput({"class": "form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    price = forms.DecimalField(widget=forms.NumberInput({"class": "form-control"}))
    quantity = forms.IntegerField(widget=forms.NumberInput({"class": "form-control"}))
    class Meta:
        model = Book
        fields = ('name','price','quantity','image','description','category')


class UserEditForm(forms.ModelForm):
    user_role = forms.CharField(widget=forms.Select(choices=User.USER_ROLE_CHOICES, attrs={"class": "form-control"}))
    class Meta:
        model = User
        fields = ['user_role']



