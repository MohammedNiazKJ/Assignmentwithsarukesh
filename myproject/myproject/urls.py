from django.urls import path
from django.contrib import admin
from .views import home_page_view, to_do_list, download_data, res, login, task_list, add_task, edit_task, delete_task
from .views import home_page_view, to_do_list, download_data, res

urlpatterns = [
    path('', home_page_view, name='home'),
    path('admin/', admin.site.urls),
    path('todo/', to_do_list, name='todo'),
    path('download_data/', download_data, name='download_data'),
    path('res/', res, name='res'), 
    # path('welcome/', welcome, name='welcome'),
    path('login/', login, name='login'),
    path('task/', task_list, name='task'),
    path('addtask/', add_task, name='add_task'),
    path('edit/', edit_task, name='edit_task'),
    path('delete/', delete_task, name='delete_task'),
]
