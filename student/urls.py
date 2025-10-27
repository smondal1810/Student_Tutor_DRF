
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list_create, name='student-list'),
    path('<int:pk>/', views.student_detail, name='student-detail'),
]
