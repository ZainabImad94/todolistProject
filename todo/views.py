from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


# Create your views here.


def todo_list(request):
    tasks = Task.objects.order_by('title')
    return render(request, 'todo/todo_list.html', {'tasks': tasks})


def task_new(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            return redirect('todo_list')
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            return redirect('todo_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/add_task.html', {'form': form})


def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('todo_list')


def done(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = True
    task.save()
    return redirect('todo_list')


def undone(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = False
    task.save()
    return redirect('todo_list')
