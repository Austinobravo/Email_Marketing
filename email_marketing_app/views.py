from smtplib import SMTPConnectError, SMTPSenderRefused
import socket
from urllib.error import URLError
from django.forms import ValidationError
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from .models import Email, Visitor
from django.template.loader import render_to_string, get_template
import pandas as pd
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import  MyForm
import json

# Create your views here.

def visitor_count(request):
    count = Visitor.objects.count()
    return render(request, 'visitor_count.html', {'count': count})

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

# @background(schedule=60 * 60 * 24)  # Schedule every 24 hours
def send_batch_email(subject, message, from_email, emails, files=None):
    try:
        email_count = len(emails)  # Calculate the number of emails
        for email_address, name in emails:
            context = {'name': name, 'message': message}
            template_message = get_template('email.html').render(context)
            email = EmailMessage(subject, template_message, from_email, [email_address])
            email.content_subtype = 'html'
            if files:
                for file in files:
                    email.attach(file.name, file.read(), file.content_type)
            # email.send()
        return email_count

        # logger.info(f'Sent {email_count} emails in the batch')  # Log the email count
    except Exception as e:
       return "An error occurred "


def custom_message(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            # message = bleach.clean(form.cleaned_data['message'], tags=[], strip=True)
            message = form.cleaned_data['message']
            subject = request.POST.get('subject')
            from_email = request.POST.get('from_email')
            uploaded_file = request.FILES['file']
            files = request.FILES.getlist('Attach_file')

                # Check the file type based on the file extension
            if uploaded_file.name.endswith('.xlsx'):
                data = pd.read_excel(uploaded_file, engine='openpyxl', encoding='utf-8')
                # data = pd.read_excel(uploaded_file) 
            elif uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file, encoding='utf-8')
                # data = pd.read_csv(uploaded_file)
            else:
                messages.info(request, "Unsupported file type")
                return redirect('error')

            if 'customer_email' not in data.columns:
                messages.info(request,'Your file has no "customer_email" field.')
                return redirect('error')
            
            if 'customer_last_name' not in data.columns:
                messages.info(request,'Your file has no "customer_last_name" field.')
                return redirect('error')
            
            emails = [(row['customer_email'], row['customer_last_name']) for _, row in data.iterrows()][:100]
            # Pass data from the request to the background task
            # first_hundred_emails = emails[:100]
            sent_emails = []
            for email_address, name in emails:
                try:
                    email_count = len(sent_emails) + 1  # Calculate the number of emails
                    context = {'name': name, 'message': message}
                    template_message = get_template('email.html').render(context)
                    email = EmailMessage(subject, template_message, from_email, [email_address])
                    email.content_subtype = 'html'
                    if files:
                        for file in files:
                            email.attach(file.name, file.read(), file.content_type)
                    email.send()
                    sent_emails.append(email_address)


                except BadHeaderError:
                    messages.error(request, 'Invalid header found in email')
                    return redirect('error')
                except socket.gaierror as dns_error:
                    messages.error(request, 'No DNS network connection')
                    print(str(dns_error)) 
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
                    send_error = e  # Get the error message as a string
                    errors_body = send_error.body
                    error_response_str = errors_body.decode('utf-8')
                    error_response_dict = json.loads(error_response_str)
                    # Access the dictionary
                    errors = error_response_dict.get("errors")[0]["message"] 
                    messages.error(request, "An error occurred")
                    context = {"emails": sent_emails, 'sent': email_count,'error': errors}
                    return render(request, 'error.html', context) 
            context = {"emails": sent_emails, 'sent': email_count,}
            messages.success(request, f'Sent {email_count} emails in the batch')
            return render(request, 'success.html', context )
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
