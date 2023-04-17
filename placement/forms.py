from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class NewUserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'roll_number', 'department', 'course', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserSignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        print(user)
        if commit:
            try:
                user.save()
            except:
                print("Failed")
        return user

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'profile_pic', 'roll_number', 'department', 'course', 'contact', 'year_of_passing', 'placed_company', 'package', 'offer_type')

    def clean_email(self):
        if self.instance: 
            return self.instance.email
        else: 
            return self.fields['email']

#class StudentForm(forms.Form):
 #   first_name = forms.CharField(max_length=50)
 #   last_name = forms.CharField(max_length=50)
    # email = forms.EmailField()
    # phone_number = forms.CharField(max_length=20)
    # date_of_birth = forms.DateField()
    # address = forms.CharField(widget=forms.Textarea)

# from django import forms

# class FormPageone(forms.Form):
#     name = forms.CharField(label='Name', max_length=100)
#     email = forms.EmailField(unique=True)
#     roll_number = forms.CharField(max_length=10, blank=True, null=True)
#     placedcompany = forms.CharField(label='Placed Company', max_length=100)
#     package = forms.IntegerField(label='Package', max_length=12)
#     offertype = forms.CharField(label='Offer Type', max_length=30)
#     noofrounds = forms.IntegerField(label='Number of Rounds', max_length=10)

# class FormPagetwo(forms.Form):
#     photo=forms.ImageField(upload_to ='uploads/% Y/% m/% d/')
#     successquote=forms.CharField(label='Success Quote', max_length=100)
