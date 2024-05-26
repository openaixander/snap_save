from django.shortcuts import render, redirect


from .forms import PhotoRegistrationForm, ClientRegistrationForm
from .models import Account

# refactored functions
from .refactored_functions import send_activation_link, send_password_reset_link, decode_uid
import requests
from django.contrib.auth.decorators import login_required
# what i need for the email activation
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages, auth
# from django.http import HttpResponse
# Create your views here.



def register_photographer(request):
    if request.method != 'POST':
        # if the form is not post, then just submit an empty form, then render the form again due to error from the field or non-field error
        form = PhotoRegistrationForm()
    else:
        # submit the data that was submitted via post request
        form = PhotoRegistrationForm(request.POST)
        if form.is_valid():
            try:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                bank_number = form.cleaned_data['bank_number']
                password = form.cleaned_data['password']
                
                username = email.split('@')[0]
                
                # Need to make the necessary fields, then assign them to the account model, which it will create a user for us
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                
                # Save additional fields
                user.phone_number = phone_number
                user.bank_number = bank_number
                user.save()
                
                # Call the function to send activation link
                send_activation_link(request, user, email, 'photographer')
                return redirect('/accounts/login/?command=verification&email='+email)
            
            except Exception:
                messages.error(request, 'An error occurred during registration.')
                return redirect('accounts:register_photographer')
            
    context = {
        'form': form,
    }
    return render(request, 'accounts/p_registration.html', context)



def register_client(request):
    # check if the request is whether a post or get 
    if request.method != 'POST':
        # send out the form again to them to fill in
        form = ClientRegistrationForm()
    else:
        form = ClientRegistrationForm(request.POST)
        # now checks, if the form is valid, then a client account will be created and an activation link will be sent
        if form.is_valid():
            try:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number= form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                
                username = email.split('@')[0]
                
                # now after this, a user will be created
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                # now after all this been created, then assigned the phone number to the phone number field in the database
                user.phone_number = phone_number
                user.save()
                
                # now we call the send_activation link to send email to our user
                send_activation_link(request, user, email, 'client')
                return redirect('/accounts/login/?command=verification&email='+email)
            except Exception:
                messages.error(request, 'An error occurred during registration.')
                return redirect('accounts:register_client')
            
    context = {
        'form': form,
    }
            
    return render(request, 'accounts/c_registration.html', context)




def activate(request, uidb64, token, account_type):
    """
    Activate the user account using the provided UID, token, and account type.

    Args:
        request (HttpRequest): The HTTP request object.
        uidb64 (str): The base64 encoded UID.
        token (str): The activation token.
        account_type (str): The type of account to activate ('photographer' or 'client').

    Returns:
        HttpResponseRedirect: Redirects to the appropriate page after activation.
    """
    # Decode the UID from base64
    uid = decode_uid(uidb64)

    # If UID decoding fails, show error message and redirect
    if not uid:
        messages.error(request, 'Invalid activation link: User does not exist.')
        return redirect('photo_template:selection')

    try:
        # Get the user with the decoded UID
        user = Account._default_manager.get(pk=uid)
    except Account.DoesNotExist:
        # If user does not exist, show error message and redirect
        messages.error(request, 'Invalid activation link: User does not exist.')
        return redirect('photo_template:selection')

    # If user account is already active, show warning message
    if user.is_active:
        messages.warning(request, 'Your account has already been activated.')
    # If activation token is valid, activate user account
    elif default_token_generator.check_token(user, token):
        user.is_active = True
        if account_type == 'photographer':
            user.is_photographer = True
        elif account_type == 'client':
            user.is_client = True
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
    else:
        # If activation token is invalid, show error message and redirect
        messages.error(request, 'Invalid activation link: The token is invalid')
        return redirect('photo_template:selection')

    # Redirect to the appropriate page after activation
    if user.is_photographer:
        return redirect('photo_template:p_dashboard')
    elif user.is_client:
        return redirect('photo_template:c_dashboard')



# THIS IS THE LOGIN VIEW
def login(request):
    # Check if the request method is POST (i.e., form submission)
    if request.method == 'POST':
        # Extract email and password from the submitted form
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Authenticate the user with the provided email and password
            user = auth.authenticate(email=email, password=password)
            # If authentication is successful (i.e., user exists and provided correct credentials)
            if user is not None:
                # Log in the user
                auth.login(request, user)
                # Get the URL of the previous page (if available)
                url = request.META.get('HTTP_REFERER')
                try:
                    # If the previous page URL exists
                    if url:
                        # Parse the query parameters from the URL
                        query = requests.utils.urlparse(url).query
                        # Extract query parameters and store them in a dictionary
                        params = dict(x.split('=') for x in query.split('&'))
                        # If 'next' parameter is present in the query parameters
                        if 'next' in params:
                            # Redirect the user to the page specified in the 'next' parameter
                            next_page = params['next']
                            return redirect(next_page)
                # Handle exceptions related to URL parsing or redirection
                except Exception as e:
                    pass

                if user.is_photographer:
                    # Display a success message and redirect the user to the default page
                    messages.success(request, f'Welcome to your dashboard, {user.first_name}.')
                    return redirect('photo_template:p_dashboard')
                if user.is_client:
                    messages.success(request, f'Welcome to your dashboard, {user.first_name}.')
                    return redirect('photo_template:c_dashboard')
                
            else:
                # If authentication fails, display an error message and redirect back to the login page
                messages.error(request, 'Invalid login credentials!')
                return redirect('accounts:login')
        # Handle any exceptions that might occur during the login process
        except Exception as e:
            messages.error(request, 'An error occurred during login. Please try again later.')
            return redirect('accounts:login')
    
    # Render the login form template for GET requests
    return render(request, 'accounts/login.html')

@login_required()
def logout(request):
    auth.logout(request)
    messages.info(request, f'You have logged out. Visit us again.')
    return redirect('accounts:login')



# THIS IS THE FORGOT_PASSWORD VIEW
def forgot_password(request):
    # checks if the data is submitted via POST request
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # when the email is gotten, we check our database and see whether that email exists or not
        if Account.objects.filter(email=email).exists():
            # if a user with that email exists, then get the email with the exact wording
            user = Account.objects.get(email__exact=email)
            
            # now it checks the flags whether that user is a photographer or a client
            
            if user.is_photographer:
                # now we send an email with the encrypted primary key of the user to their email
                # this function will send the encrypted primary key
                send_password_reset_link(request, user, email, 'photographer')
                pass
            elif user.is_client:
                # now we send an email with the encrypted primary key of the user to their email
                # this function will send the encrypted primary key
                send_password_reset_link(request, user, email, 'client')
                pass
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('accounts:login')
        
        # if the user doesn't exist, then send them a message to notify them
        else:
            messages.error(request, 'User does not exist!')
            return redirect('accounts:login')
    return render(request, 'accounts/forgot_password.html')



def reset_password_validate(request, uidb64, token, account_type):
    """
    Validate the password reset link.

    Args:
        request (HttpRequest): The HTTP request object.
        uidb64 (str): The base64 encoded UID of the user.
        token (str): The password reset token.
        account_type (str): The type of account ('photographer' or 'client').

    Returns:
        HttpResponse: Redirects to the appropriate page based on validation results.
    """
    # Decode the UID from base64
    uid = decode_uid(uidb64)

    # If UID decoding fails, show error message and redirect
    if not uid:
        messages.error(request, 'Invalid activation link: User does not exist.')
        return redirect('photo_template:selection')

    try:
        # Get the user with the decoded UID
        user = Account._default_manager.get(pk=uid)
    except Account.DoesNotExist:
        # If user does not exist, show error message and redirect
        messages.error(request, 'Invalid activation link: User does not exist.')
        return redirect('photo_template:selection')

    # Check if the user is of the correct account type
    if account_type == 'photographer' and not user.is_photographer:
        messages.error(request, 'Invalid activation link: Account type mismatch.')
        return redirect('photo_template:selection')
    elif account_type == 'client' and not user.is_client:
        messages.error(request, 'Invalid activation link: Account type mismatch.')
        return redirect('photo_template:selection')

    # Check if the token is valid for the user
    if user is not None and default_token_generator.check_token(user, token):
        # Save the user ID in the session
        request.session['uid'] = uid
        messages.info(request, 'Reset your password.')
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('accounts:forgot_password')

    
    
    
def reset_password(request):
    # check whether it is a post request
    # get the password and the confirmed password
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        
        # check if password is longer than 8 and is the same with the confirmed password
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('accounts:reset_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('accounts:reset_password')
        
        
        try:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
        except Account.DoesNotExist:
            messages.error(request, 'Invalid user for password reset.')
            return redirect('accounts:register')
        
        user.set_password(password)
        user.save()
        messages.success(request, 'Password reset successful. You can now login with your new password.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/reset_password.html')