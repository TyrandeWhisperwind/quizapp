from django.urls import include, path
from . import views

#add app name for namespace to work
app_name = 'candidates'
urlpatterns = [
    #path to the folder containing the home view and the eexecuted function
    path('', views.candidates_list,name="candidateurl"), 

]
