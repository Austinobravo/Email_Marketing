from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from .models import Email
from django.template.loader import render_to_string, get_template
import pandas as pd

from .forms import ContactForm
# Create your views here.

def index(request):
    return render(request, 'index.html')

def sendMail(request):
    mail = Email.objects.all()
    for user in mail:
        address = user.email_address
    
        message = "We have new products"
        subject = "New Products"
        context = {'name': user.name, 'message': message }
        message = get_template('email.html').render(context)
        email = EmailMessage(subject, message, 'Marketing Team', [address])
        email.content_subtype= 'html'
        email.send()
    return redirect('index')

def sendMailInactive(request):
    mail = Email.objects.filter(status='inactive')
    for user in mail:
        address = user.email_address
    
        message = "We have new products"
        subject = "New Products"
        context = {'name': user.name, 'message': message }
        message = get_template('email.html').render(context)
        email = EmailMessage(subject, message, 'Marketing Team', [address])
        email.content_subtype= 'html'
        email.send()
    return redirect('index')

def sendMailActive(request):
    mail = Email.objects.filter(status='active')
    for user in mail:
        address = user.email_address
    
        message = "We have new products"
        subject = "New Products"
        context = {'name': user.name, 'message': message }
        message = get_template('email.html').render(context)
        email = EmailMessage(subject, message, 'Marketing Team', [address])
        email.content_subtype= 'html'
        email.send()
    return redirect('index')

def custom_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        subject = request.POST.get('subject')

        uploaded_file = request.FILES['file']

            # Check the file type based on the file extension
        if uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
        else:
            return HttpResponse("Unsupported file type")

    
        for _, row in data.iterrows():
            email_address = row['Emails']
            name = row['Names']
        # print(address)
        
            context = {'name': name, 'message': message }
            message = get_template('email.html').render(context)
            email = EmailMessage(subject, message, 'austinobravo@gmail.com', [email_address])
            email.content_subtype= 'html'
            print('email',email_address)
            print('name',name)
            print('message',message)
            print('subject',subject)
            email.send()
            return redirect('index')
        # return render(request, 'message.html')
    else:
        form = ContactForm()
        return render(request, 'message.html', {'form': form})

 
