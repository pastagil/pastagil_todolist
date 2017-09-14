from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasklist/home.html', {'tasks': tasks})
    
    
class TaskListView(ListView):
    model = Task
    template_name = "tasklist/task_list.html"
    context_object_name = "tasks"
    

class TaskCreateView(SuccessMessageMixin,CreateView):
    model = Task
    template_name = "tasklist/task_create.html"
    success_message = 'Tarea Creada Exitosamente :D'
    form_class = TaskForm
    success_url = reverse_lazy("tasklist:task_list")
    

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasklist/task_delete.html"
    success_url = reverse_lazy("tasklist:task_list")
    success_message = "Tarea Eliminada Exitosamente :D"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message )
        return super(TaskDeleteView, self).delete(request, *args, **kwargs)
    
class TaskUpdateView(SuccessMessageMixin,UpdateView):
    model = Task
    template_name = "tasklist/task_edit.html"
    success_message = 'Tarea Editada Exitosamente :D'
    fields = '__all__'
    success_url = reverse_lazy("tasklist:task_list")
