from django.shortcuts import render
from exams.models import Candidate
from django.shortcuts import render

def candidates_list(request):
    candidates=Candidate.objects.all()
    return render(request,'candidates/candidate_list.html',{'candidates':candidates})
