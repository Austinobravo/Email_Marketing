from django.db import models
from django_summernote.fields import SummernoteTextField

# Create your models here.
customer_status = (
    ('active','active'),
    ('inactive', 'inactive')
)

class Email(models.Model):
    name = models.CharField(max_length=200)
    email_address = models.EmailField()
    status = models.CharField(max_length=50,choices=customer_status, default='active')

    def __str__(self):
        return self.name
    
class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.ip_address

class MyModel(models.Model):
    message = SummernoteTextField()
