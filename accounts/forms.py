from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.models import User
from exams.models import Candidate

class CandidateForm(UserCreationForm):
    firstName =forms.CharField(max_length=50)
    lastName = forms.CharField(max_length=50)
    phoneNumber = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=70)
    class Meta(UserCreationForm.Meta):
        model = User
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        candidate = Candidate.objects.create(user=user)
        candidate.firstName=self.cleaned_data.get('firstName')
        candidate.lastName=self.cleaned_data.get('lastName')
        candidate.phoneNumber=self.cleaned_data.get('phoneNumber')
        candidate.email=self.cleaned_data.get('email')
        candidate.save()
        return user
