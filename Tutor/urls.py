
# from django.urls import path
# from .views import (
#     EmpoyeesClass, EmployeeDetailClass,
#     EmployeeSlotCreate, AvailableSlotsList, BookSlot
# )

# urlpatterns = [
#     path('', EmpoyeesClass.as_view(), name='employee-list'),
#     path('<int:pk>/', EmployeeDetailClass.as_view(), name='employee-detail'),
#     path('<int:emp_id>/slots/', EmployeeSlotCreate.as_view(), name='create-slot'),
#     path('slots/available/', AvailableSlotsList.as_view(), name='available-slots'),
#     path('slots/book/<int:slot_id>/<int:student_id>/', BookSlot.as_view(), name='book-slot'),
# ]

from django.urls import path
from .views import (
    EmpoyeesClass, EmployeeDetailClass,
    EmployeeSlotCreate, AvailableSlotsList, BookSlot
)

urlpatterns = [
    path('', EmpoyeesClass.as_view(), name='employee-list'),
    path('<int:pk>/', EmployeeDetailClass.as_view(), name='employee-detail'),
    path('<int:emp_id>/slots/', EmployeeSlotCreate.as_view(), name='create-slot'),
    path('slots/available/', AvailableSlotsList.as_view(), name='available-slots'),
    path('slots/book/<int:slot_id>/', BookSlot.as_view(), name='book-slot'),
]
