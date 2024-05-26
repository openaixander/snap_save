from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def decode_uid(uidb64):
    """
    Decode the UID from base64.

    Args:
        uidb64 (str): The base64 encoded UID.

    Returns:
        str or None: The decoded UID if successful, otherwise None.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        return uid
    except (TypeError, ValueError, OverflowError):
        return None


def send_activation_link(request, user, email, account_type):
    """
    Send an activation link to the user's email address.

    Args:
        request (HttpRequest): The HTTP request object.
        user (Account): The user object for whom the activation link is being sent.
        email (str): The email address of the user.
        account_type (str): The type of account ('photographer' or 'client').

    Returns:
        None
    """
    try:
        current_site = get_current_site(request)
        # Once the current site is obtained, send the activation email
        mail_subject = 'Please activate your account.'
        context_string = {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'user_type': account_type  # Add the account type parameter
        }
        message = render_to_string('accounts/account_verification_email.html', context_string)
        to_email = email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()
    except:
        # Handle exceptions if necessary
        pass
    
    
def send_password_reset_link(request, user, email, account_type):
    """
    Send a reset password activation link to the user's email address.

    Args:
        request (HttpRequest): The HTTP request object.
        user (Account): The user object for whom the activation link is being sent.
        email (str): The email address of the user.
        account_type (str): The type of account ('photographer' or 'client').

    Returns:
        None
    """
    try:
        current_site = get_current_site(request)
        # Once the current site is obtained, send the activation email
        mail_subject = "Please reset your account's password."
        context_string = {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'user_type': account_type  # Add the account type parameter
        }
        message = render_to_string('accounts/reset_password_link.html', context_string)
        to_email = email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.send()
    except:
        # Handle exceptions if necessary
        pass