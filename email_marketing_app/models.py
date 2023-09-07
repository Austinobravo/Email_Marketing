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
    
# models.py


class MyModel(models.Model):
    title = models.CharField(max_length=100)
    message = SummernoteTextField()
