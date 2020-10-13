from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('task/new/', views.task_new, name='task_new'),
    path('task/edit/<pk>', views.task_edit, name='task_edit'),
    path('task/delete/<pk>', views.task_delete, name='task_delete'),
    path('done/<pk>', views.done, name='done'),
    path('undone/<pk>', views.undone, name='undone'),

]
