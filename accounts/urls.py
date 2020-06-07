from django.conf.urls import  url
from . import views
#namespace used for urls to separate the urls of the different apps in case there is same urlname
app_name = 'accounts'
urlpatterns = [
    #the function executed to list the exams and the name of the url in the htnl template
    url(r'^signup/$', views.signup_view,name='signup'),
    url(r'^login/$', views.login_view,name='login'),
    url(r'^logout/$', views.logout_view,name='logout'),

]
