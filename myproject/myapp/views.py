from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse, HttpResponseNotAllowed, FileResponse, HttpResponse
from .serializer import UserSerializer
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os
import json


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    response = Response({"token": token.key, "user": serializer.data})
    response.set_cookie(key="token", value=token.key)  # Set token in cookie
    return redirect("/")


def home_page_view(request):
    today = datetime.today()
    formatted_datetime = today.strftime("%d-%m-%y <br><br> %h-%m")
    return HttpResponse(formatted_datetime)


from django.http import JsonResponse, HttpResponseNotAllowed


@csrf_exempt
def document_download(request):
    file_path = "documentation.docx"
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = 'attachment; filename="documentation.docx"'
        return response
    else:
        return HttpResponse("File not found", status=404)


# def to_do_list(request):
#     if request.method == 'POST':
#         try:
#             # Check Content-Type header
#             content_type = request.headers.get('Content-Type', '')
#             if 'application/json' not in content_type:
#                 return JsonResponse({'success': False, 'message': 'Request must be JSON'}, status=400)

#             data = json.loads(request.body)
#             task=data.get('task')
#             title = data.get('title')
#             due_date = data.get('due_date')
#             if title  and due_date  and task :
#                    try:
#                       datetime.strptime(due_date,'%Y-%m-%d')
#                    except ValueError:
#                       return JsonResponse({'sucess':False, 'message': 'invalid ddue date format.Please provide due date in YYYY-MM-DD format'}, status=400)
#                    print("Received name:", task,title,due_date )
#                    return JsonResponse({'success': True, 'message': 'task and title and due date are stored successfully'})
#             else:
#                    return JsonResponse({'success': False, 'message': 'no task or title or due date given'}, status=400)
#         except ValueError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
#     elif request.method == 'GET':
#          return JsonResponse({'success': True, 'message': 'Data stored'})
#     else:
#         return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import os
from django.conf import settings  # Import Django settings

JSON_FILE_PATH = "tasks.json"
BASE_DIRECTORY = os.path.join(settings.BASE_DIR, "myproject")


@csrf_exempt
def to_do_list(request):
    if request.method == "GET":
        tasks = list_saved_files()
        name = request.GET.get("name", None)
        description = request.GET.get("description", None)
        status = request.GET.get("status", None)
        priority = request.GET.get("priority", None)
        filtered_tasks = filter_tasks(tasks, name, description, status, priority)
        return JsonResponse({"success": True, "tasks": filtered_tasks})

    elif request.method == "POST":
        try:
            content_type = request.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                return JsonResponse(
                    {"success": False, "message": "Request must be JSON"}, status=400
                )
            data = json.loads(request.body)
            task_name = data.get("task_name")
            description = data.get("description")
            status = data.get("status")
            priority = data.get("priority")
            due_date = data.get("due_date")
            if not task_name or not due_date:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Task name and due date are required",
                    },
                    status=400,
                )
            try:
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                if due_date < datetime.now().date():
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "The due date cannot be in the past",
                        },
                        status=400,
                    )
            except ValueError:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid due date format. Please provide a date in the format YYYY-MM-DD.",
                    },
                    status=400,
                )
            task_data = {
                "task_name": task_name,
                "description": description,
                "status": status,
                "priority": priority,
                "due_date": due_date.strftime("%Y-%m-%d"),
            }
            save_task(task_name, task_data)
            return JsonResponse(
                {"success": True, "message": "Task stored successfully"}
            )
        except ValueError:
            return JsonResponse(
                {"success": False, "message": "Invalid JSON data"}, status=400
            )

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            task_name = data.get("task_name")
            if not task_name:
                return JsonResponse(
                    {"success": False, "message": "Task name not provided"}, status=400
                )
            tasks_data = list_saved_files()  # Remove the unnecessary argument
            for task_filename, task_data in tasks_data.items():
                if task_data.get("task_name") == task_name:
                    task_data.update(data)
                    due_date = task_data.get("due_date")
                    if not due_date:
                        return JsonResponse(
                            {"success": False, "message": "Due date not provided"},
                            status=400,
                        )
                    try:
                        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                        if due_date < datetime.now().date():
                            return JsonResponse(
                                {
                                    "success": False,
                                    "message": "The due date cannot be in the past",
                                },
                                status=400,
                            )
                    except ValueError:
                        return JsonResponse(
                            {
                                "success": False,
                                "message": "Invalid due date format. Please provide a date in the format YYYY-MM-DD.",
                            },
                            status=400,
                        )
                    success, message = save_task(task_name, task_data)
                    if success:
                        return JsonResponse({"success": True, "message": message})
                    else:
                        return JsonResponse(
                            {"success": False, "message": message}, status=400
                        )
            return JsonResponse(
                {"success": False, "message": "Task not found"}, status=404
            )
        except ValueError as e:
            return JsonResponse(
                {"success": False, "message": f"Invalid JSON data: {e}"}, status=400
            )
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            task_name = data.get("task_name")
            if not task_name:
                return JsonResponse(
                    {"success": False, "message": "Task name not provided"}, status=400
                )
            filename = f"{task_name}.json"
            if os.path.exists(os.path.join(BASE_DIRECTORY, filename)):
                os.remove(os.path.join(BASE_DIRECTORY, filename))
                return JsonResponse(
                    {"success": True, "message": "Task deleted successfully"}
                )
            else:
                return JsonResponse(
                    {"success": False, "message": "Task not found"}, status=404
                )
        except ValueError as e:
            return JsonResponse(
                {"success": False, "message": f"Invalid JSON data: {e}"}, status=400
            )
    else:
        return HttpResponseNotAllowed(["GET", "POST", "PUT", "DELETE"])


def filter_tasks(tasks, name=None, description=None, status=None, priority=None):
    filtered_tasks = []
    for filename, file_data in tasks.items():
        task = file_data
        if name and name.lower() not in task.get("task_name", "").lower():
            continue
        if (
            description
            and description.lower() not in task.get("description", "").lower()
        ):
            continue
        if status and task.get("status") != status:
            continue
        if priority and task.get("priority") != priority:
            continue
        filtered_tasks.append(task)
    return filtered_tasks


def remaining_time(due_date):
    current_date = datetime.now().date()
    remaining = due_date - current_date
    return remaining.days


def list_saved_files():
    saved_files_data = {}
    try:
        for filename in os.listdir(BASE_DIRECTORY):
            if filename.endswith(".json"):
                file_path = os.path.join(BASE_DIRECTORY, filename)
                with open(file_path, "r") as f:
                    file_data = json.load(f)
                    if "due_date" in file_data:
                        due_date = datetime.strptime(
                            file_data["due_date"], "%Y-%m-%d"
                        ).date()
                        file_data["remaining_time"] = remaining_time(due_date)
                saved_files_data[filename] = file_data
    except FileNotFoundError:
        print(
            f"Error: The directory {BASE_DIRECTORY} does not exist or is not accessible."
        )
    return saved_files_data


def save_task(task_name, task_data):
    filename = f"{task_name}.json"
    try:
        with open(os.path.join(BASE_DIRECTORY, filename), "w") as file:
            json.dump(task_data, file)
        return True, "Task saved successfully"
    except Exception as e:
        return False, f"Error saving task {task_name}: {e}"
