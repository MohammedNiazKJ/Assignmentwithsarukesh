# from asyncio import Task
# import os
# import json
# from django.http import HttpResponse
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime 
# from django.http import FileResponse
# from rest_framework.decorators import api_view
# from django.shortcuts import render
# from rest_framework.response import Response
# from django.shortcuts import redirect 
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from django.http import JsonResponse
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
 
# from django.shortcuts import render

# @csrf_exempt
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])

# def home_page_view(request):
#     today = datetime.today()
#     formatted_date = today.strftime("%d-%m-%y")
#     return HttpResponse(formatted_date)

# @csrf_exempt
# def to_do_list(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             name = data.get('name')
#             email = data.get('email')
#             id = data.get('id')
#             title = data.get('title')
#             due_date = data.get('due_date')
#             if name and id and title and due_date:
#                 print("Received name:", name, email)
#                 return JsonResponse({'success': True, 'message': 'Name stored successfully'})
#             else:
#                 return JsonResponse({'success': False, 'message': 'No email or name provided'}, status=400)
#         except ValueError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
#     elif request.method == 'GET':
#         # Handle GET request here, you can return some data or an empty response
#         return JsonResponse({'success': True, 'message': 'GET request received'})
#     else:
#         return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

# def download_data(request):
#     try:
#         file_path = "Z:\Tuke FAP\pvjc-2024-khaleel-jameel\myproject\myproject\Documentation.odt"
#         if os.path.exists(file_path):
#             return FileResponse(open(file_path, 'rb'), as_attachment=True)
#         else:
#             return HttpResponse("File not found", status=404)
#     except Exception as e:
#         return HttpResponse(str(e), status=500)
    
# def res(request):
#     return render(request, 'home.html')

# @csrf_exempt

# @login_required
# def welcome(request):
#     return render(request, 'task_list.html', {'username': request.user.username})

# @login_required
# def task_list(request):
#     tasks = Task.objects.all()
#     return render(request, 'task_list.html', {'tasks': tasks})

# @login_required
# def add_task(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#     else:
#         form = TaskForm()
#     return render(request, 'task_list.html', {'form': form})

# @login_required
# def edit_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#     else:
#         form = TaskForm(instance=task)
#     return render(request, 'task_list.html', {'form': form})

# @login_required
# def delete_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     task.delete()
#     return redirect('task_list')

   
# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#         user_token = token.key
#         return HttpResponseRedirect('/task_list/')
#     else:
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

import os
import json
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User  # Import User model if needed

@csrf_exempt
@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def home_page_view(request):
    today = datetime.today()
    formatted_date = today.strftime("%d-%m-%y")
    return HttpResponse(formatted_date)

@csrf_exempt
def to_do_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            id = data.get('id')
            title = data.get('title')
            due_date = data.get('due_date')
            if name and id and title and due_date:
                print("Received name:", name, email)
                return JsonResponse({'success': True, 'message': 'Name stored successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'No email or name provided'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'success': True, 'message': 'GET request received'})
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def download_data(request):
    try:
        file_path = "Z:/Tuke FAP/pvjc-2024-khaleel-jameel/myproject/myproject/Documentation.odt"
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        else:
            return HttpResponse("File not found", status=404)
    except Exception as e:
        return HttpResponse(str(e), status=500)

def res(request):
    return render(request, 'home.html')

# @login_required
# def welcome(request):
#     return render(request, 'task_list.html', {'username': request.user.username})

@login_required
def task_list(request):
    # Assuming Task is a model defined in your Django app
    # tasks = Task.objects.all()  # Uncomment and replace Task with your actual model
    tasks = []  # Placeholder for tasks
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_list.html', {'form': form})

@login_required
def edit_task(request, task_id):
    # Assuming Task is a model defined in your Django app
    # task = Task.objects.get(id=task_id)  # Uncomment and replace Task with your actual model
    task = None  # Placeholder for task
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_list.html', {'form': form})

@login_required
def delete_task(request, task_id):
    # Assuming Task is a model defined in your Django app
    # task = Task.objects.get(id=task_id)  # Uncomment and replace Task with your actual model
    task = None  # Placeholder for task
    task.delete()
    return redirect('task_list')
@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        user_token = token.key
        return HttpResponseRedirect('/task_list/')
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from
cryptography.fernet
import
Fernet




def
keygen():

    return
Fernet.generate_key()




def
write_key_to_file(key,
filename):

    with
open(filename,
"wb")
as
key_file:

        key_file.write(key)




def
load_key_from_file(filename):

    with
open(filename,
"rb")
as
key_file:

        return
key_file.read()




def
encrypt_file(filename,
key):

    fernet
=
Fernet(key)

    with
open(filename,
"rb")
as
file:

        original_data
=
file.read()

    encrypted_data
=
fernet.encrypt(original_data)

    with
open(filename
+
".encrypted",
"wb")
as
encrypted_file:

        encrypted_file.write(encrypted_data)


def decrypt_file(encrypted_filename,key):

    fernet = Fernet(key)
    with open(encrypted_filename,"rb") as file:

        encrypted_data
=
file.read()

    decrypted_data
=
fernet.decrypt(encrypted_data)

    decrypted_filename
=
encrypted_filename.replace(".encrypted",
"_decrypted.txt")

    with
open(decrypted_filename,
"wb")
as
decrypted_file:

        decrypted_file.write(decrypted_data)




