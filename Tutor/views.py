# from django.shortcuts import render

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import EmployeeModel, TimeSlotModel
# from .serializers import EmployeeSerializer, TimeSlotSerializer
# from student.models import StudentModel

# class EmpoyeesClass(APIView):
#     def get(self, request):
#         employee = EmployeeModel.objects.all()
#         serializer = EmployeeSerializer(employee, many = True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = EmployeeSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class EmployeeDetailClass(APIView):
    
    
    
#     def get_object(self, pk):
#         try:
#             return EmployeeModel.objects.get(pk = pk)
            
#         except EmployeeModel.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
            
#     def get(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     def put(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(instance=employee, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
            
    
        
    
            
        

# class EmployeeSlotCreate(APIView):
#     def post(self, request, emp_id):
#         try:
#             employee = EmployeeModel.objects.get(pk=emp_id)
#         except EmployeeModel.DoesNotExist:
#             return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

#         slot = request.data.get('slot')
#         if TimeSlotModel.objects.filter(employee=employee, slot=slot).exists():
#             return Response({"message": "Slot already exists"}, status=status.HTTP_400_BAD_REQUEST)

#         slot_obj = TimeSlotModel.objects.create(employee=employee, slot=slot)
#         serializer = TimeSlotSerializer(slot_obj)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# # Get all available slots (for students)
# class AvailableSlotsList(APIView):
#     def get(self, request):
#         slots = TimeSlotModel.objects.filter(is_booked=False)
#         serializer = TimeSlotSerializer(slots, many=True)
#         return Response(serializer.data)


# # Student books a slot
# class BookSlot(APIView):
#     def post(self, request, slot_id, student_id):
#         try:
#             slot = TimeSlotModel.objects.get(pk=slot_id)
#         except TimeSlotModel.DoesNotExist:
#             return Response({"error": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

#         if slot.is_booked:
#             return Response({"message": "This slot is already booked"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             student = StudentModel.objects.get(pk=student_id)
#         except StudentModel.DoesNotExist:
#             return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

#         slot.is_booked = True
#         slot.booked_by = student
#         slot.save()

#         serializer = TimeSlotSerializer(slot)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import EmployeeModel, TimeSlotModel, Booking
from .serializers import EmployeeSerializer, TimeSlotSerializer, BookingSerializer
from student.models import StudentModel
from accounts.permissions import IsTutor, IsStudent
from rest_framework.permissions import IsAuthenticated

class EmpoyeesClass(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        employee = EmployeeModel.objects.all()
        serializer = EmployeeSerializer(employee, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Only tutor or admin can create employees? If creating via admin, skip permission
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailClass(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return EmployeeModel.objects.get(pk = pk)
        except EmployeeModel.DoesNotExist:
            return None

    def get(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(instance=employee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeSlotCreate(APIView):
    permission_classes = [IsAuthenticated, IsTutor]

    def post(self, request, emp_id):
        # ensure that the authenticated user is the owner of this employee (tutor)
        try:
            employee = EmployeeModel.objects.get(pk=emp_id)
        except EmployeeModel.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        # If the employee is linked to a user (tutor), ensure same user
        if employee.user and employee.user != request.user:
            return Response({"error":"You are not allowed to create slots for this tutor"}, status=status.HTTP_403_FORBIDDEN)

        slot = request.data.get('slot')
        if TimeSlotModel.objects.filter(employee=employee, slot=slot).exists():
            return Response({"message": "Slot already exists"}, status=status.HTTP_400_BAD_REQUEST)

        slot_obj = TimeSlotModel.objects.create(employee=employee, slot=slot)
        serializer = TimeSlotSerializer(slot_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Get all available slots (for students)
class AvailableSlotsList(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        # A slot is available if bookings < 10
        slots = TimeSlotModel.objects.all()
        available = []
        for s in slots:
            if s.bookings.count() < 10:
                available.append(s)
        serializer = TimeSlotSerializer(available, many=True)
        return Response(serializer.data)


# Student books a slot using authenticated student (no student_id in URL)
class BookSlot(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, slot_id):
        try:
            slot = TimeSlotModel.objects.get(pk=slot_id)
        except TimeSlotModel.DoesNotExist:
            return Response({"error": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

        student_profile = getattr(request.user, 'student', None)
        if not student_profile:
            return Response({"error": "Student profile not found"}, status=status.HTTP_403_FORBIDDEN)

        # check if student already booked this slot
        if Booking.objects.filter(timeslot=slot, student=student_profile).exists():
            return Response({"message": "You already booked this slot"}, status=status.HTTP_400_BAD_REQUEST)

        current_bookings = slot.bookings.count()
        if current_bookings >= 10:
            return Response({"message": "This slot is fully booked"}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(timeslot=slot, student=student_profile)
        serializer = TimeSlotSerializer(slot)
        return Response(serializer.data, status=status.HTTP_200_OK)
