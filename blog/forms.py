from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile, Posts
from django.utils import timezone



class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=['username','email']


class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields =['image']

class UpdatePost(forms.ModelForm):
	class Meta:
		model=Posts
		fields=['title','content']
	
	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)

	