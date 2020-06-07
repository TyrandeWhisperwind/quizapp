from django.urls import include, path
from . import views
from django.conf.urls import  url

#namespace used for urls to separate the urls of the different apps in case there is same urlname
app_name = 'exams'
urlpatterns = [
    #the function executed to list the exams and the name of the url in the htnl template
    path('', views.exams_list,name='examurl'),
    #we capture that variabl and name it pk with <> and send it to the function in the view
    path('<int:pk>/',views.take_exam,name='detailurlexam'),
    path('exams_crud/', views.exams_crud,name='examcrud'),
    path('exams_crud/add_exam/', views.ExamCreateView.as_view(), name="add_exam"),
    path('exams_crud/<int:pk>/question_add/', views.question_add, name='question_add'),
    path('exams_crud/<int:quiz_pk>/<int:pk>/', views.CreateOrderView.as_view(), name='question_change'),
    path('exams_crud/<int:pk>/', views.question_list, name='question_list'),
    path('exams_crud/<int:pk>/updatequest/', views.CreateOrderView.as_view(), name='question_upd'),
    path('exams_crud/newexam/', views.ExamCreateView.as_view(), name='addex'),







]
