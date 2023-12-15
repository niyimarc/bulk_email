from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Breader
import os
from dotenv import load_dotenv
load_dotenv()
get_from_email = os.environ.get('EMAIL_HOST_USER')
developer_name = os.environ.get('DEVELOPER_NAME')
business_name = os.environ.get('BUSINESS_NAME')
whatsapp_link = os.environ.get('WHATSAPP_LINK')
whatsapp_number = os.environ.get('WHATSAPP_NUMBER')
contact_email = os.environ.get('CONTACT_EMAIL')
from_email = business_name + "<" + get_from_email + ">"

def send_email_view(request, pk):
    breader = get_object_or_404(Breader, pk=pk)
    # Reset the is_email_sent field to False before sending the email
    breader.is_email_sent = False
    breader.save()

    subject = 'Elevate Your Pet Business with a Personalized Website'
    message = ''
    recipient_list = [breader.email]
    context = {
        'title': subject,
        'user': breader.user,
        'pet_name': breader.pet_name, 
        'platform': breader.platform,
        'whatsapp_link': whatsapp_link,
        'whatsapp_number': whatsapp_number,
        'business_name': business_name,
        'contact_email': contact_email,
        'business_name': business_name,
        'developer_name': developer_name
    }
    html_message = render_to_string('mail_app/email_templates/breader.html', context)
    if breader.status:
        if not breader.is_email_sent:
            send_mail(
                subject, 
                message, 
                from_email, 
                recipient_list,
                fail_silently=False,
                html_message=html_message,
                )

            # Update the Breader instance to mark the email as sent
            breader.is_email_sent = True
            breader.number_of_email_sent += 1
            breader.save()

        return HttpResponse("Email sent successfully")
    else:
        return HttpResponse("Email not sent because user status is deactivated")
