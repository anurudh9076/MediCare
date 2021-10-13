from django import forms
from django.forms import ModelForm
from .models import Doctor,User


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        #field = "__all__"
        fields = ( 'age', 'mobNum','profilePicture','speciality','city','availability')
        labels ={
            'age': 'age',
            'username': 'username',
            'city': 'city',
            'profilePicture': 'profilepic',
            'speciality':'speciality',
            'availability':'availibility',
        }
        # widgets = {
        #     'user': forms.TextInput(attrs={'class':'form-control','placeholder':'user'}),
        #     'age': forms.TextInput(attrs={'class':'form-control','placeholder':'age'}),
        #     'mobNum': forms.TextInput(attrs={'class':'form-control','placeholder':'mobNum'}),
        #     'profilePicture': forms.ImageField(attrs={'class':'form-control','placeholder':'profilePicture'}),
        #     'speciality': forms.PasswordInput(attrs={'class':'form-control','placeholder':'speciality'}),
            
        # }



class UserForm(ModelForm):
    class Meta:
        model = User
        #field = "__all__"
        fields = ('first_name', 'last_name', 'username','email','password')
        labels ={
            'first_name': '',
            'last_name': '',
            'username': '',
            'manager': '',
            'email': '',
            'password':'',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'first_name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'last_name'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'password': forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),
            
        }
