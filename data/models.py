from django.db import models

# Create your models here.
class Data(models.Model):
    operating_system = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    system_port = models.CharField(max_length=255)
    system_owner = models.CharField(max_length=255)
    system_username = models.CharField(max_length=255)
    system_password = models.CharField(max_length=255)
    system_description = models.CharField(max_length=255)
    server_name = models.CharField(max_length=255)
    last_change_date = models.DateField(auto_now=True)
