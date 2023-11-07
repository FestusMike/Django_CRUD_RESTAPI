from django.db import models

# Create your models here.

class UserData(models.Model):
    First_name = models.CharField(blank=False, max_length=25)
    Last_name = models.CharField(blank=False, max_length=25)
    Age = models.IntegerField(blank=False)
    email_address = models.EmailField(unique=True, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.First_name

    class Meta:
        db_table = 'apidata'

