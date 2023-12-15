from django.contrib import admin
from .models import Breader
from django.core.mail import send_mail
from django.utils.html import format_html
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib.admin import SimpleListFilter
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

class NumberEmailSentFilter(SimpleListFilter):
    title = 'Number of Email Sent'
    parameter_name = 'number_of_email_sent'

    def lookups(self, request, model_admin):
        return [
            ('0-0', '0'),
            ('1-1', '1'),
            ('2-5', '1-5'),
            ('6-10', '6-10'),
            ('11-15', '11-15'),
            ('16-20', '16-20'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            min_value, max_value = map(int, value.split('-'))
            return queryset.filter(number_of_email_sent__gte=min_value, number_of_email_sent__lte=max_value)
        return queryset

    
class BreaderAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'pet_name', 'is_email_sent', 'number_of_email_sent', 'status', 'send_email_button')
    list_filter = ('status', 'is_email_sent', NumberEmailSentFilter)
    readonly_fields = ('is_email_sent', 'number_of_email_sent')
    actions = ['send_bulk_email']
    def send_email_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Send Email</a>',
            reverse('send_email', args=[obj.pk])
        )

    send_email_button.short_description = 'Send Email'
    send_email_button.allow_tags = True

    def send_bulk_email(modeladmin, request, queryset):

        for breader in queryset:
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

        # Redirect back to the Breader admin page
        return HttpResponseRedirect(reverse('admin:mail_app_breader_changelist'))

    send_bulk_email.short_description = "Send Email to selected Breader instances"

admin.site.register(Breader, BreaderAdmin)