# from django.db import models

# class StudentModel(models.Model):
    
#     name = models.CharField(max_length=100)
#     roll_number = models.IntegerField()
#     dept_id = models.CharField(max_length=10)
    
    
#     def __str__(self):
#         return self.name
from django.db import models
from django.conf import settings

class StudentModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='student')
    name = models.CharField(max_length=100)
    roll_number = models.IntegerField()
    dept_id = models.CharField(max_length=10)

    def __str__(self):
        return self.name

