from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage



def send_token(request, email, token):
    try:
        current_site = get_current_site(request)
        mail_subject = "Here's your token for the folder you created."
        context_string = {
            'domain': current_site.domain,
            'token': token,
        }
        message = render_to_string('folders/send_folder_token.html', context_string)
        send_email = EmailMessage(mail_subject, message, to=[email])
        send_email.content_subtype = "html"
        send_email.send()
    except Exception as e:
        pass
        