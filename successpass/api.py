from rest_framework import routers
from exams import api_views

router = routers.DefaultRouter()
router.register(r'exams', api_views.ExamViewset)
router.register(r'questions', api_views.QuestionsViewset)
router.register(r'options', api_views.OptionsViewset)
router.register(r'candidate', api_views.CandidateViewset)
router.register(r'candidateResponse', api_views.CandidateResponseViewset)
