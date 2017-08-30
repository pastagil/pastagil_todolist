from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm


def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasklist/home.html', {'tasks': tasks})
    
    
class TaskListView(ListView):
    model = Task
    template_name = "tasklist/task_list.html"
    context_object_name = "tasks"
    

class TaskCreateView(CreateView):
    model = Task
    template_name = "tasklist/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasklist:task_list")
    

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasklist/task_delete.html"
    success_url = reverse_lazy("tasklist:task_list")
    
    
class TaskUpdateView(UpdateView):
    model = Task
    template_name = "tasklist/task_edit.html"
    fields = '__all__'
    success_url = reverse_lazy("tasklist:task_list")