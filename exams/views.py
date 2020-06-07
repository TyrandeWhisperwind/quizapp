from .models import Exam, Questions, Options, Candidate,CandidateResponse,TakenExam
from django.forms import inlineformset_factory
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
from . import forms


from extra_views import InlineFormSetFactory, CreateWithInlinesView,UpdateWithInlinesView



#python manage.py migrate --run-syncdb  if the django doesnt recognize created tables via the python migrate  cmd

def paginatedItems(request,items,numberItem):
    paginator=Paginator(items,numberItem)
    page = request.GET.get('page')
    posts=paginator.get_page(page)
    return (posts)

#show list of exams for a candidate
#this decorator will add more functionalities to my function in oder to protect it
@login_required(login_url='/accounts/login/')
def exams_list(request):
    candidate = get_object_or_404(Candidate, pk=request.user.id)

    candidate=Candidate.objects.get(pk=request.user.id)
    exams=candidate.exams.all()
        #order the items!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return render(request,'exams/exams_list.html',{'items': exams})


@login_required(login_url='/accounts/login/')
def take_exam(request, pk):
    #get list of exams
    #if fisrt time entering the quiz
    exam = get_object_or_404(Exam, pk=pk)
    #get id of logged candidate
    candidate = request.user.candidate
    #order the items!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    unanswered_questions = candidate.get_unanswered_questions(exam)
    posts=paginatedItems(request,unanswered_questions,2)

    if TakenExam.objects.filter(candidate=candidate,exam=exam,date_begin__isnull=True):
        TakenExam.objects.filter(candidate=candidate,exam=exam).update(date_begin=datetime.now())

    #for http://127.0.0.1:8080/exams/1
    if  request.method == 'GET':
        if candidate.exams.filter(pk=pk).exists():
            return render(request, 'exams/exams_detail.html', { 'exam': exam ,'items':posts})

    #if clicked on submit
    if  request.method == 'POST':
        question = get_object_or_404(Questions, pk=request.POST.get('question_id'))
        some_var = request.POST.getlist('choice')
        if len(some_var)> 0:
            selected_choice = question.options_set.filter(pk__in=some_var)

            answers_list = list(selected_choice)
            for item in answers_list:
                foo = CandidateResponse.objects.create(question=question,chosen_option=item,candidate=candidate)
                foo.save()
                #update this table TakenExam score and date of started and end of exam!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


            if candidate.get_unanswered_questions(exam).exists():
                next = request.POST.get('next')
                messages.success(request, ('Answer saved'))
                return redirect(next)
            else:
                candidate.calculate_score(exam)


                return redirect('exams:examurl')


        else:
            next = request.POST.get('next')
            messages.error(request, ('No option chosen!'))
            return redirect(next)

    return render(request, 'exams/exams_detail.html', {
        'exam': exam,
        'items':posts}
    )



def exams_crud(request):
    exams=Exam.objects.all()
    return render(request,'exams/exams_crud.html',{'items':exams})


def exam_add(request):
    if request.method == 'POST':
        form = forms.ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exams:examcrud')
    else:
        form = forms.ExamForm()

    return render(request, 'exams/exam_add.html', {
                  'form': form})


def question_add(request, pk):
    quiz = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('exams:examcrud')
    else:
        form = forms.QuestionForm()

    return render(request, 'exams/question_add_form.html', {'quiz': quiz, 'form': form})

# exam questions and options are nested
# first user create an exam
#then he ll add a question to that exam
# after adding a question he can change it to add options with function below that uses inlineformset_factory to link options to the question
#needs pk of exam and pk of qurstion
#{"username": "useqwee", "password": "1234abcd", "firstName": "qweqweabcd", "lastName": "eqwqweqabcd", "phoneNumber": "112312313", "email": "qwqweeq@gmail.com"}

def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Exam, pk=quiz_pk)
    question = get_object_or_404(Questions, pk=question_pk, exam=quiz_pk)
    AnswerFormSet = inlineformset_factory(
        Questions,  # parent model
        Options,  # base model
        formset=forms.BaseAnswerInlineFormSet, #rewrite clean method to check if he chosed at least one correct answer
        fields=('body', 'image','is_correct',),
        min_num=2,
        validate_min=True,
        extra=10,
        validate_max=True
    )
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST, instance=question)#post here is to get the data and associate it with the instance to commit changes to it
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            #always use atomic transaction in case saving two different objects related by ForeignKey
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect(reverse('exams:question_list', kwargs={"pk": quiz_pk}))
    else:
        form = forms.QuestionForm(instance=question)#in update forms we must send the instance back
        formset = AnswerFormSet(instance=question)

    return render(request, 'exams/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })

def question_list(request, pk):
    questions=Questions.objects.filter(exam=pk)
    return render(request,'exams/questions_list.html',{'items': questions,'pk':pk})


#case 3 nested i can start creating exams and questions
#then if selected question create updatequestioninline and inlineformsetfactory of options
#then of option has ForeignKey make list of options of question then when clicked on option possibility of update it and adding the nested form
############################################################################################
class QuestionInline(InlineFormSetFactory):
    model = Questions
    fields = '__all__'

class ExamCreateView(CreateWithInlinesView):
    model = Exam
    inlines = [QuestionInline,]
    fields = '__all__'
    template_name = 'exams/crt.html'
    success_url = '/'
    factory_kwargs = {'extra': 0}


class OptionsInline(InlineFormSetFactory):
    model = Options
    fields = '__all__'

class CreateOrderView(UpdateWithInlinesView):
    model = Questions
    inlines = [OptionsInline,]
    fields = '__all__'
    template_name = 'exams/updatequest.html'
    success_url = '/'
    factory_kwargs = {'extra': 0}



from django.views.generic import TemplateView, ListView, CreateView

QuestionsInlineFormSet = inlineformset_factory(Exam, Questions,fields='__all__', extra=1, can_delete=False)
OptionsInlineFormSet = inlineformset_factory(Questions, Options,fields='__all__', extra=1, can_delete=False)


class ExamCreateView(CreateView):
    model = Exam
    fields='__all__'
    template_name = 'exams/tem.html'
    factory_kwargs = {'extra': 0}
    success_url = '/'

    def form_valid(self, form):
        result = super(ExamCreateView, self).form_valid(form)

        questions_formset = QuestionsInlineFormSet(form.data, instance=self.object, prefix='questions_formset')
        if questions_formset.is_valid():
            questions = questions_formset.save()

        questions_count = 0
        for question in questions:
            options_formset = OptionsInlineFormSet(form.data, instance=question, prefix='options_formset_%s' % questions_count)
            if options_formset.is_valid():
                options_formset.save()
            questions_count += 1

        return result

    def get_context_data(self, **kwargs):
        context = super(ExamCreateView, self).get_context_data(**kwargs)
        context['authors_formset'] = QuestionsInlineFormSet(prefix='questions_formset')
        context['books_formset'] = OptionsInlineFormSet(prefix='options_formset_0')
        return context
