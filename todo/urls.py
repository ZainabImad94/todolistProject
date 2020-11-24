from django.urls import path
from . import views
from accounts.views import update_profile

urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list'),  # view the tasks list
    path('/create/', views.TaskCreate.as_view(), name='task_new'),
    path('/task/edit/<pk>', views.TaskUpdate.as_view(), name='task_edit'),  # edit an existing task
    path('/task/delete/<pk>', views.TaskDelete.as_view(), name='task_delete'),  # delete a task
    path('/done/<pk>', views.TaskComplete.as_view(), name='done'),  # to make the task complete
    path('/undone/<pk>', views.TaskIncomplete.as_view(), name='undone'),  # to make the task uncompleted
    path('/details/<pk>', views.TaskDetail.as_view(), name='task_detail'),
    path('/view/<pk>', views.TaskView.as_view(), name='task_view'),
    path('/profile/', update_profile, name='setting_profile'),

]
