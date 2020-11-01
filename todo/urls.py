from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),  # view the tasks list
    path('task/new/', views.task_new, name='task_new'),  # make a new task
    path('task/edit/<pk>', views.task_edit, name='task_edit'),  # edit an existing task
    path('task/delete/<pk>', views.task_delete, name='task_delete'),  # delete a task
    path('done/<pk>', views.done, name='done'),  # to make the task complete
    path('undone/<pk>', views.undone, name='undone'),  # to make the task uncompleted

]
