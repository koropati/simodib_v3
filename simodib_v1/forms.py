from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.utils import timezone
from .models import Kurir, User, Manager, Rice

class KurirSignUpForm(UserCreationForm):
    email = forms.EmailField()
    no_hp = forms.CharField()
    alamat = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name','last_name','password1','password2',)
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_kurir = True
        user.created_date = timezone.now()
        user.save()
        kurir = Kurir.objects.create(user=user,email=self.cleaned_data['email'],no_hp=self.cleaned_data['no_hp'],alamat=self.cleaned_data['alamat'], created_date=timezone.now(), status_akun='0')
        return user

class ManagerSignUpForm(UserCreationForm):
    email = forms.EmailField()
    no_hp = forms.CharField()
    alamat = forms.CharField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','first_name','last_name','password1','password2',)
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
            manager = Manager.objects.create(user=user,email=self.cleaned_data['email'],no_hp=self.cleaned_data['no_hp'],alamat=self.cleaned_data['alamat'], created_date=timezone.now())
        return user

class RiceAddForm(forms.ModelForm):
    class Meta:
        model : Rice
        fields = ('name', 'stock', 'price',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nama/Varietas'}),
            'stock': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Stock Beras/Kwintal'}),
            'price': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Harga Beras/Kwintal'}),
        }