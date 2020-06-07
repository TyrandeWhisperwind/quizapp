from django.contrib import admin
from django.urls import path,include
from django.conf.urls import  include
from .api import router
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
 path('admin/', admin.site.urls),
 path('nested_admin/', include('nested_admin.urls')),
 path('api/v1/', include(router.urls)), #routers for the Restframework

 #path home and its view
 path('', views.home,name='homeurl'),
 #urls of exams app
 #and name space specification for the templates path to make links between the html pages (templates)
 path('exams/', include('exams.urls',namespace="exams")),
 #urls of candidates app
 #and name space specification for the templates path to make links between the html pages (templates)
 path('candidates/', include('candidates.urls',namespace="candidates")),

 path('accounts/', include('accounts.urls',namespace="accounts")),

 # path to admin adding apps for the oautho2
 path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
 # Authentication user resframework
 path('register/', views.register),
 path('token/', views.token),
 path('token/refresh/', views.refresh_token),
 path('token/revoke/', views.revoke_token),

]

urlpatterns += staticfiles_urlpatterns()
