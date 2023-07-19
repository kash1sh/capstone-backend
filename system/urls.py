from django.urls import path
from .views import index,SpecificMentorView,SpecificPatientView,UserRegistrationView,ScoreBoardView,get_read_score,rapid_color_naming
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', index, name = "index"),
    path('register/', UserRegistrationView.as_view(), name = "register"),
    path('mentor/',SpecificMentorView.as_view(),name = "mentor"),
    path('patient/',SpecificPatientView.as_view(),name = "patient"),
    path('login/',obtain_auth_token,name = "login"),
    path('score/',ScoreBoardView.as_view(),name = "score"),

    ## All Tests 
    path('read/',get_read_score,name="read"),
    path('color/',rapid_color_naming,name="color")
]
