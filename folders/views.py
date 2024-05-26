from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Folder, UploadFile
from .forms import FolderCreationForm, UploadFileForm, UploadZipForm
from photo_template.decorators import photographer_required
from .reused_func import send_token


from django.http import HttpResponse
from django.http import JsonResponse

# for the zip file, It seems I really need to import lots of dependecies
import zipfile #importing the zipfile module to handle ZIP file operations
import os #importing os module to handle file and directory paths
from django.conf import settings #importing this to use the django settings

# Create your views here.


@login_required
@photographer_required
def create_folder(request):
    # to get rid of the not null constraint, we need to set the owner field to the logged in user
    user = request.user
    token = None
    # for one to create a folder, we need to check whether if the request is a get or post request
    if request.method != 'POST':
        # send out the form again as it is not a POST request
        form = FolderCreationForm()
    else:
        # accept the form with the data that it has been submitted with
        form = FolderCreationForm(request.POST)
        # print(form)
        # now we need to check to see if the form is valid
        if form.is_valid():
            # use the try-except block
            try:
                # now, we get the the two fields and save them in variables
                name = form.cleaned_data['name']
                price = form.cleaned_data['price']
                # this here is written like this because, in case a user intentionally left the field empty, a default string is provided which won't cause error
                description = form.cleaned_data.get('description', '')
                # now after this, we call the folder class to make an instance of it
                folder = Folder.objects.create(name=name, price=price, owner=user, description=description)
                folder.save()
                token = folder.token  # Get the generated token for the folder
                
                # send a token to the user email
                send_token(request, user.email, token)
                # send a message to the user notify them that a token has been generated for them for that specific folder
                messages.success(request, f'A token for {folder.name} has been generated for you. Please check your email')
                # Pass the token to the context
                context = {
                    'form': FolderCreationForm(),
                    'token': token
                }
                return render(request, 'folders/create_folder.html', context)
            except Exception as e:
                print(e)
    context = {
        'form':form,
        'token':token
    }
    return render(request, 'folders/create_folder.html', context)


@login_required
@photographer_required
def upload_images(request):
    return render(request, 'folders/upload_images.html')


@login_required
@photographer_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            folder = form.cleaned_data['folder']
            files = form.cleaned_data['images']

            for file in files:
                UploadFile.objects.create(owner=request.user, folder=folder, image=file)

            return JsonResponse({'success': True})  # Return JSON response
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = UploadFileForm()

    context = {
        'form': form
    }
    return render(request, 'folders/upload_file.html', context)


@login_required
@photographer_required
def upload_zip(request):
    if request.method != 'POST':
        # return the form back to the user
        form = UploadZipForm()
    
    else:
        form = UploadZipForm(request.POST, request.FILES) #Initializing the form with the POST data and uploaded
        # checking if the form is valid
        if form.is_valid():
            try:
                zip_instance = form.save(commit=False) #saving the form but not committing to the database yet
                zip_instance.owner = request.user # Setting the owner of the ZIP file to the current user
                zip_instance.save() # Saving the ZIP file instance to the database
                
                return redirect('folders:upload_zip')
            except:
                pass
    context = {
        'form':form
    }        
    return render(request, 'folders/upload_zip.html', context)


