from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.db.models import Sum


class Exam(models.Model):
 title = models.CharField(max_length=1000,blank=True)
 duration = models.DurationField(default=timedelta(), blank=True, null=False)
 beginDate = models.DateTimeField(null=True,blank=True)
 endDate = models.DateTimeField(null=True,blank=True)
 percentage = models.FloatField(default=0,null=False,blank=True)
 maxNumberCandidate = models.IntegerField(default=0,null=True,blank=True)
 def __str__(self):
  return self.title
 def questions_of_exam(self):
  return self.questions_set.all()

#######################################################################
class Questions(models.Model):
 title = models.CharField(max_length=1000)
 description = models.CharField(max_length=1000,blank=True)
 exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
 weight = models.FloatField()
 types= (
   ('radio', 'radio'),
   ('checkbox', 'multi-select')
)
 contentType = models.CharField(choices=types, max_length=128)
 def __str__(self):
  return self.title

 def options_of_question(self):
  return self.options_set.all()
#####################################################################
class Options(models.Model):
 question = models.ForeignKey(Questions, on_delete=models.CASCADE)
 body = models.CharField(max_length=100000)
 image = models.ImageField(default=False,blank=True)
 is_correct = models.BooleanField('Correct answer', default=False)

 def __str__(self):
  return self.body
#####################################################################
class Candidate(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
 exams = models.ManyToManyField(Exam,blank=True,through='TakenExam')
 firstName = models.CharField(max_length=50)
 lastName = models.CharField(max_length=50)
 phoneNumber = models.CharField(max_length=50)
 email = models.EmailField(max_length=70)
 def __str__(self):
  return self.user.username
 def get_unanswered_questions(self, exam):
        #get all the the chosen_options of a candidate by  exam_answers
        #get the questions of the chosen_options by the candidate for that exam and list the questions related to the filtereed answers
        answered_questions = self.exam_answers.filter(chosen_option__question__exam=exam).values_list('chosen_option__question__pk', flat=True)
        #exclude answerd questions
        questions = exam.questions_set.exclude(pk__in=answered_questions)

        return questions
def calculate_score(self, exam):
        correct_answers = self.exam_answers.filter(chosen_option__question__exam=exam, chosen_option__is_correct=True).values_list('chosen_option__question__pk', flat=True)
        #get the list of correctly answerd questions by id case questions_multiselect
        questions_multiselect = exam.questions_set.filter(pk__in=correct_answers,contentType="checkbox").values_list('pk', flat=True)
        #get the list of correctly answerd questions by id case radio queryset
        questions_radio=exam.questions_set.filter(pk__in=correct_answers,contentType="radio")
        #sum up questions_radio weight
        q=questions_radio.aggregate(Sum('weight'))

        weight=0.0
        for item in questions_multiselect:
            correct_options=Options.objects.filter(question=item,is_correct=True).values_list('pk', flat=True)
            correct_answers_ofq = self.exam_answers.filter(chosen_option__question=item, chosen_option__is_correct=True).values_list('chosen_option__pk', flat=True)
            #case all correct
            if len(correct_options)==len(correct_answers_ofq):
                weight+=Questions.objects.get(pk=item).weight
            #case some then devide weight by 2
            elif(len(correct_options)!=len(correct_answers_ofq)):
                weight+=Questions.objects.get(pk=item).weight/2.0

        #total weight of exam goten from questions
        totalP=Questions.objects.filter(exam=exam).aggregate(Sum('weight'))
        percentage=round((q['weight__sum']+weight)/totalP['weight__sum'], 2)
        TakenExam.objects.filter(candidate=self.pk,exam=exam).update(percentage= percentage, date_finish=datetime.now())
        return ("done")

#####################################################################
class TakenExam(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    date_begin = models.DateTimeField(null=True,blank=True)
    date_finish = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.exam.title + "/" +  self.candidate.user.username

#####################################################################
class CandidateResponse(models.Model):
 question = models.ForeignKey(Questions, on_delete=models.CASCADE)
 chosen_option = models.ForeignKey(Options,on_delete=models.CASCADE,null=True,blank=True)
 candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE,related_name='exam_answers')
 def __str__(self):
  return self.question.title + "/" +  str(self.chosen_option.pk)
#####################################################################
