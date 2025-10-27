# from rest_framework import serializers
# from .models import EmployeeModel, TimeSlotModel



# class EmployeeSerializer(serializers.ModelSerializer):
#      class Meta:
#          model = EmployeeModel
#          fields = '__all__'
         

# class TimeSlotSerializer(serializers.ModelSerializer):
#     employee_name = serializers.CharField(source='employee.emp_name', read_only=True)
#     student_name = serializers.CharField(source='booked_by.name', read_only=True)

#     class Meta:
#         model = TimeSlotModel
#         fields = ['id', 'employee', 'employee_name', 'slot', 'is_booked', 'booked_by', 'student_name']
         
from rest_framework import serializers
from .models import EmployeeModel, TimeSlotModel, Booking


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.emp_name', read_only=True)
    student_name = serializers.CharField(source='booked_by.name', read_only=True)

    class Meta:
        model = TimeSlotModel
        fields = ['id', 'employee', 'employee_name', 'slot', 'is_booked', 'booked_by', 'student_name']


class BookingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    tutor_name = serializers.CharField(source='timeslot.employee.emp_name', read_only=True)
    slot = serializers.CharField(source='timeslot.slot', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'student', 'student_name', 'tutor_name', 'slot', 'created_at']
