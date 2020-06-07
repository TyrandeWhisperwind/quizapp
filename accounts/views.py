from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout


def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect('homeurl')


def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            #redirect user to login
            user = form.get_user()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            #check where the user was trying to go with the next value in the url
            if 'next' in request.POST:
                #'next' is the name of the input in the html
                return redirect(request.POST.get('next'))
            else:
                return redirect('exams:examurl')
    else:
        form=AuthenticationForm()
    return render(request,'accounts/login.html',{'form':form})


def signup_view(request):
    if request.method=='POST':
        #getting the passed values in the request and putting them in a new form
        #to check if it is valid or nop
        form=forms.CandidateForm(request.POST)
        if form.is_valid():
            #save user in database plus
            #log user in after signinup....
            user=form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            #app name plus the name of the url in the view
            return redirect('exams:examurl')
        else:
            form = forms.CandidateForm()
            return render(request, 'accounts/signup.html', { 'form': form})
    #if method is get then send the forms
    #if the form is not valid it ll resend the form also
    else:
        #instanciate a form
        form = forms.CandidateForm()
    #send the form the the html template
    return render(request,'accounts/signup.html',{'form' :form})
