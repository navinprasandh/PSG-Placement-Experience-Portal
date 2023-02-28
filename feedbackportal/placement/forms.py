# from django import forms
# from django.contrib.auth.forms import UserCreationForm
#from placement.models import Student

# class SignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)
    
#     class Meta:
#         model = Student
#         fields = ['roll_number', 'email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super(SignupForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user

#class StudentForm(forms.Form):
 #   first_name = forms.CharField(max_length=50)
 #   last_name = forms.CharField(max_length=50)
    # email = forms.EmailField()
    # phone_number = forms.CharField(max_length=20)
    # date_of_birth = forms.DateField()
    # address = forms.CharField(widget=forms.Textarea)