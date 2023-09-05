from django.db import models

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