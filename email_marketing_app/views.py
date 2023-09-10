from smtplib import SMTPConnectError, SMTPSenderRefused
import socket
from urllib.error import URLError
from django.forms import ValidationError
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from .models import Email
from django.template.loader import render_to_string, get_template
import pandas as pd
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import  MyForm
import bleach
# Create your views here.


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
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            message = bleach.clean(form.cleaned_data['message'], tags=[], strip=True)
            subject = request.POST.get('subject')
            from_email = request.POST.get('from_email')
            uploaded_file = request.FILES['file']
            files = request.FILES.getlist('Attach_file')

                # Check the file type based on the file extension
            if uploaded_file.name.endswith('.xlsx'):
                    data = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
            else:
                messages.info(request, "Unsupported file type")
                return redirect('error')
            
            if 'Emails' not in data.columns:
                messages.info(request,'Your file has no "Emails" field.')
                return redirect('error')
            
            if 'Names' not in data.columns:
                messages.info(request,'Your file has no "Names" field.')
                return redirect('error')
                
        
            for _, row in data.iterrows():
                email_address = row['Emails']
                name = row['Names']

                try:
                    context = {'name': name, 'message': message }
                    template_message = get_template('email.html').render(context)
                    email = EmailMessage(subject, template_message, from_email, [email_address])
                    email.content_subtype= 'html'
                    if files:
                        for file in files:
                            email.attach(file.name, file.read(), file.content_type)
                    # email.send()


                except BadHeaderError:
                    messages.error(request, 'Invalid header found in email')
                    return redirect('error')
                except socket.gaierror as dns_error:
                    messages.error(request, 'No DNS network connection')
                    return redirect('error')
                except URLError as e_error:
                    messages.error(request, 'Poor or No network connection')
                    return redirect('error')
                except ObjectDoesNotExist:
                    messages.error(request, 'Email not found')
                    return redirect('error')
                except AttributeError:
                    messages.error(request, 'Check the details you entered.')
                    return redirect('error')
                except SMTPConnectError as smtp_connect_error:
                    messages.error(request, 'Error connecting to the SMTP server')
                    return redirect('error')
                except SMTPSenderRefused as sender_refused_error:
                    messages.error(request, 'Sender not registered with the SMTP server')
                    return redirect('error')
                except Exception as e:
                    messages.error(request, "An error occured")
                    return redirect('error')

            messages.success(request, 'Emails sent successfully')
            return redirect('success')
        else:
            messages.error(request, "Your form is invalid")
            return redirect('error')
    else:
        form = MyForm()
        return render(request, 'message.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def error(request):
    return render(request, 'error.html')
