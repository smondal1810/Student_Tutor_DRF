from django.urls import path
from .views import TutorRegisterView, StudentRegisterView, LoginView

urlpatterns = [
    path('tutor/register/', TutorRegisterView.as_view(), name='tutor-register'),
    path('student/register/', StudentRegisterView.as_view(), name='student-register'),
    path('login/', LoginView.as_view(), name='login'),
]
