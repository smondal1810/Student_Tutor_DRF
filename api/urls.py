
from django.urls import path, include

urlpatterns = [
    path('students/', include('student.urls')),
    
    path('tutor/', include('Tutor.urls'))
    

]
