from django import forms
from .models import Exam, Questions, Options, Candidate,CandidateResponse,TakenExam
from django.forms.models import inlineformset_factory
from django.forms.utils import ValidationError
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from . import models


class ExamForm(forms.ModelForm):
    class Meta:
        model =Exam
        fields='__all__'




class QuestionForm(forms.ModelForm):
    class Meta:
        model =Questions
        fields='__all__'


class OptionForm(forms.ModelForm):
    class Meta:
        model =Options
        fields='__all__'




class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')
