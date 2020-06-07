"""
To support such a set of operations, DRF provides a handy tool – ViewSet. 
It takes the idea behind the standard class-based views from Django to a higher level. What it does is
packing the above set into one class with the automatic creation of appropriate URL paths.
"""

from rest_framework import viewsets
from . import models
from . import serializers

class ExamViewset(viewsets.ModelViewSet):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    
class QuestionsViewset(viewsets.ModelViewSet):
    queryset = models.Questions.objects.all()
    serializer_class = serializers.QuestionsSerializer
    
class OptionsViewset(viewsets.ModelViewSet):
    queryset = models.Options.objects.all()
    serializer_class = serializers.OptionsSerializer
    
class CandidateViewset(viewsets.ModelViewSet):
    queryset = models.Candidate.objects.all()
    serializer_class = serializers.CandidateSerializer
    
class CandidateResponseViewset(viewsets.ModelViewSet):
    queryset = models.CandidateResponse.objects.all()
    serializer_class = serializers.CandidateResponseSerializer