# from django.db import models

# class EmployeeModel(models.Model):
#     emp_name = models.CharField(max_length=80)
#     emp_id = models.IntegerField(default=0)
#     emp_dept = models.CharField(max_length=80)
    
    
#     def __str__(self):
#         return self.emp_name
    
    
# class TimeSlotModel(models.Model):
#     TIME_SLOTS = [
#         ('10AM-12PM', '10AM to 12PM'),
#         ('12PM-2PM', '12PM to 2PM'),
#         ('4PM-6PM', '4PM to 6PM'),
#         ('6PM-8PM', '6PM to 8PM'),
#     ]

#     employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='slots')
#     slot = models.CharField(max_length=20, choices=TIME_SLOTS)
#     is_booked = models.BooleanField(default=False)
#     booked_by = models.ForeignKey('student.StudentModel', on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"{self.employee.emp_name} - {self.slot}"
# from django.db import models
# from django.conf import settings

# class EmployeeModel(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='tutor')
#     emp_name = models.CharField(max_length=80)
#     emp_id = models.IntegerField(default=0)
#     emp_dept = models.CharField(max_length=80)

#     def __str__(self):
#         return self.emp_name


# class TimeSlotModel(models.Model):
#     TIME_SLOTS = [
#         ('10AM-12PM', '10AM to 12PM'),
#         ('12PM-2PM', '12PM to 2PM'),
#         ('4PM-6PM', '4PM to 6PM'),
#         ('6PM-8PM', '6PM to 8PM'),
#     ]

#     employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='slots')
#     slot = models.CharField(max_length=20, choices=TIME_SLOTS)
#     # Instead of single booked_by, we'll support multiple bookings by creating Booking model OR use a many-to-many
#     # We'll add a Booking model below if you want; for simplicity keep current fields but we will add Booking model next.
#     is_booked = models.BooleanField(default=False)
#     booked_by = models.ForeignKey('student.StudentModel', on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"{self.employee.emp_name} - {self.slot}"
    
# class Booking(models.Model):
#     timeslot = models.ForeignKey(TimeSlotModel, on_delete=models.CASCADE, related_name='bookings')
#     student = models.ForeignKey('student.StudentModel', on_delete=models.CASCADE, related_name='bookings')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('timeslot', 'student')  # a student can't book same slot twice

#     def __str__(self):
#         return f"{self.student.name} booked {self.timeslot}"
    
from django.db import models
from django.conf import settings

class EmployeeModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='tutor')
    emp_name = models.CharField(max_length=80)
    emp_id = models.IntegerField(default=0)
    emp_dept = models.CharField(max_length=80)

    def __str__(self):
        return self.emp_name


class TimeSlotModel(models.Model):
    TIME_SLOTS = [
        ('10AM-12PM', '10AM to 12PM'),
        ('12PM-2PM', '12PM to 2PM'),
        ('4PM-6PM', '4PM to 6PM'),
        ('6PM-8PM', '6PM to 8PM'),
    ]

    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='slots')
    slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey('student.StudentModel', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.employee.emp_name} - {self.slot}"


class Booking(models.Model):
    timeslot = models.ForeignKey(TimeSlotModel, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey('student.StudentModel', on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('timeslot', 'student')

    def __str__(self):
        return f"{self.student.name} booked {self.timeslot}"
