from django.conf.urls import url
from .views import home, TaskListView, TaskCreateView

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^lista$', TaskListView.as_view(), name='task_list'),
    url(r'^crear_tarea$', TaskCreateView.as_view(), name='task_create'),
]
