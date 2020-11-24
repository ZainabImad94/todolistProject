from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from .forms import TaskForm
from .models import Task
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, View
from django.contrib import messages


# Create your views here.

decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class TaskList(ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = reversed(Task.objects.filter(creator=self.request.user))
        return context


# @login_required
# def task_list(request):
#     task = reversed(Task.objects.filter(creator=request.user))
#     return render(request, 'todo/task_list.html', {'task': task})

@login_required
def save_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            if template_name == 'todo/task_create.html':
                messages.success(request, 'Your task created successfully!')
            else:
                messages.warning(request, 'Your task updated successfully!')
            data['form_is_valid'] = True
            task = reversed(Task.objects.filter(creator=request.user))
            data['html_task_list'] = render_to_string('todo/partial_task_list.html', {
                'task': task
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@method_decorator(decorators, name='dispatch')
class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return save_form(request, form, 'todo/task_create.html')

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return save_form(request, form, 'todo/task_create.html')


# @login_required
# def task_new(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#     else:
#         form = TaskForm()
#     return save_form(request, form, 'todo/add_task.html')


@method_decorator(decorators, name='dispatch')
class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return save_form(request, form, 'todo/task_update.html')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return save_form(request, form, 'todo/task_update.html')


# @login_required
# def task_edit(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     if request.method == "POST":
#         form = TaskForm(request.POST, request.FILES, instance=task)
#     else:
#         form = TaskForm(instance=task)
#     return save_form(request, form, 'todo/edit_task.html')


@method_decorator(decorators, name='dispatch')
class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    data = dict()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        self.data['html_form'] = render_to_string('todo/task_delete.html',
                                                  context,
                                                  request=request,
                                                  )
        return JsonResponse(self.data)

    def post(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        messages.error(request, 'Task deleted.')
        self.data['form_is_valid'] = True
        task = reversed(Task.objects.filter(creator=request.user))
        self.data['html_task_list'] = render_to_string('todo/partial_task_list.html', {'task': task})
        return JsonResponse(self.data)


# @login_required
# def task_delete(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     data = dict()
#     if request.method == 'POST':
#         task.delete()
#         data['form_is_valid'] = True  # This is just to play along with the existing code
#         task = reversed(Task.objects.filter(creator=request.user))
#         data['html_task_list'] = render_to_string('todo/partial_task_list.html', {'task': task})
#     else:
#         context = {'task': task}
#         data['html_form'] = render_to_string('todo/delete_task.html',
#                                              context,
#                                              request=request,
#                                              )
#     return JsonResponse(data)


# @login_required
# def done(request, pk):
#     task = Task.objects.get(pk=pk)
#     data = dict()
#     task.done = True
#     task.save()
#     task = reversed(Task.objects.filter(creator=request.user))
#     data['html_task_list'] = render_to_string('todo/partial_task_list.html', {'task': task})
#     return JsonResponse(data)


class TaskComplete(View):

    def get(self, request, pk):
        data = dict()
        task = Task.objects.get(pk=pk)
        task.done = True
        task.save()
        task = reversed(Task.objects.filter(creator=request.user))
        data['html_task_list'] = render_to_string('todo/partial_task_list.html', {'task': task})
        return JsonResponse(data)

# @login_required
# def undone(request, pk):
#     task = Task.objects.get(pk=pk)
#     data = dict()
#     task.done = False
#     task.save()
#     task = reversed(Task.objects.filter(creator=request.user))
#     data['html_task_list'] = render_to_string('todo/partial_task_list.html', {'task': task})
#     return JsonResponse(data)


class TaskIncomplete(View):

    def get(self, request, pk):
        data = dict()
        task = Task.objects.get(pk=pk)
        task.done = False
        task.save()
        task = reversed(Task.objects.filter(creator=request.user))
        data['html_task_list'] = render_to_string('todo/partial_task_list.html', {'task': task})
        return JsonResponse(data)


@method_decorator(decorators, name='dispatch')
class TaskDetail(DetailView):
    model = Task


# @login_required
# def task_detail(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     return render(request, 'todo/detail_task.html', {'task': task})


class TaskView(DetailView):
    model = Task
    data = dict()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        self.data['html'] = render_to_string('todo/task_view.html',
                                             context,
                                             request=request,
                                             )
        return JsonResponse(self.data)

# @login_required
# def task_view(request, pk):
#     data = dict()
#     task = get_object_or_404(Task, pk=pk)
#     data['html'] = render_to_string('todo/view_task.html',
#                                     {'task': task},
#                                     request=request,
#                                     )
#     return JsonResponse(data)
