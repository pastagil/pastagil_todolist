from django.conf.urls import url
from .views import home, TaskListView, TaskCreateView, TaskDeleteView, TaskUpdateView

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^lista$', TaskListView.as_view(), name='task_list'),
    url(r'^crear_tarea$', TaskCreateView.as_view(), name='task_create'),
    url(r'^eliminar_tarea/(?P<pk>\d+)/$', TaskDeleteView.as_view(), name='task_delete'),
    url(r'^editar_tarea/(?P<pk>\d+)/$', TaskUpdateView.as_view(), name='task_edit'),
]
