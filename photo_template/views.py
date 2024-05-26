from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import photographer_required, client_required
from django.contrib import messages

from folders.models import Folder
# Create your views here.


def index(request):
    return render(request, 'photo_template/index.html')


def selection(request):
    return render(request, 'photo_template/selection.html')


@login_required
@photographer_required
def p_dashboard(request):
    return render(request, 'photo_template/p_dashboard.html')


@login_required
@client_required
def c_dashboard(request):
    return render(request, 'photo_template/c_dashboard.html')

def search_token(request):
    return render(request, 'photo_template/search_token.html')

def searched_folder(request):
    if request.method == 'POST':
    # we now check if the request if it is a post request.
        token = request.POST.get('token')
        # getting the value that is in the name attribute
        try:
            folder = Folder.objects.get(token__exact=token)
            # the moment the user inserts the token, we update the trial field in the database
            folder.increment_token_usage
            
            # check if the token is expired after incrementing
            if folder.is_token_expired:
                messages.error(request, 'The token has expired.')
                return redirect('photo_template:c_dashboard')
            else:
                # render the search results
                context = {
                    'folder': folder,
                }
            return render(request, 'photo_template/searched_folder.html', context)
        except Folder.DoesNotExist:
            messages.error(request, 'Invalid token. Please try again.')
            return redirect('photo_template:c_dashboard')
    else:
        return render(request, 'photo_template/searched_folder.html')

