from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from .models import Task
from .views import TaskListView, TaskCreateView, TaskDeleteView, TaskUpdateView
from random import shuffle
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your tests here.


class TaskModelTest(TestCase):
    
    
    def setUp(self):
        self.description = "afeitar el gato"
    
    
    def testCreate(self):
        #given
        initial_count = Task.objects.all().count()
        #when
        task = Task.objects.create(description=self.description)
        #then
        final_count = Task.objects.all().count()
        task = Task.objects.get(description = self.description)
        self.assertEqual(initial_count+1,final_count)
        self.assertEqual(task.description, self.description)
        
        
    def testDelete(self):
        #given
        task = Task.objects.create(description=self.description)
        initial_count = Task.objects.all().count()
        #when
        Task.objects.get(description=self.description).delete()
        #then
        final_count = Task.objects.all().count()
        self.assertEqual(initial_count-1,final_count)
        self.assertEqual(Task.objects.filter(description=self.description).exists(), False)
    
    
    def testList(self):
        # given
        task_list = [
            Task(description = self.description+' 1'),
            Task(description = self.description+' 2'),
            Task(description = self.description+' 3'),
        ]
        for task in task_list:
            task.save()
        # when
        retrieved_tasks = list(Task.objects.all())
        retrieved_tasks.reverse()
        # then
        for task in task_list:
            self.assertTrue(task in retrieved_tasks)

    def testEdit(self):
        #given
        task_list = [
            Task(description = self.description+' 1'),
            Task(description = self.description+' 2'),
            Task(description = self.description+' 3'),
        ]
        for task in task_list:
            task.save()
        new_description = "afeitar al perro"
        #when
        task_to_edit = task_list[1]
        task_to_edit.description = new_description
        task_to_edit.save()
        task_edited = Task.objects.get(pk = task_to_edit.pk)
        #then
        self.assertEquals(task_edited.description, new_description)
        
    def testComplete(self):
        #given
        task_changed = Task.objects.create(description=self.description)
        task_unchanged = Task.objects.create(description=self.description)
        num_of_completed_tasks_before = Task.objects.filter(complete = True).count()
        #when
        task_changed.complete = True
        task_changed.save()
        #then
        task_changed = Task.objects.get(id = task_changed.id)
        task_unchanged = Task.objects.get(id = task_unchanged.id)
        num_of_completed_tasks_after = Task.objects.filter(complete = True).count()
        self.assertEquals(task_changed.complete, True)
        self.assertEquals(task_unchanged.complete, False)
        self.assertEquals(num_of_completed_tasks_after, num_of_completed_tasks_before + 1)


class TaskInterfaceTest(TestCase):
    
    def testCompleteListInterface(self):
        """Test if you can get a list of tasks through the list view"""
        # given:
        self.description="afeitar el gato"
        task_list = [
            Task(description = self.description+' 1', complete = True),
            Task(description = self.description+' 2'),
            Task(description = self.description+' 3'),
        ]
        for task in task_list:
            task.save()
        # when:
        request = RequestFactory().get(reverse('tasklist:task_list'))
        response = TaskListView.as_view()(request)
        # then:
        self.assertEquals(response.status_code, 200)
        for task in task_list:
            self.assertContains(response, "<del>")
            self.assertContains( response, task.description)
    
    def testIncompleteListInterface(self):
        """Test if you can get a list of tasks through the list view"""
        # given:
        self.description="afeitar el gato"
        task_list = [
            Task(description = self.description+' 1'),
            Task(description = self.description+' 2'),
            Task(description = self.description+' 3'),
        ]
        for task in task_list:
            task.save()
        # when:
        request = RequestFactory().get(reverse('tasklist:task_list'))
        response = TaskListView.as_view()(request)
        # then:
        self.assertEquals(response.status_code, 200)
        for task in task_list:
            self.assertNotContains(response, "<del>")
            self.assertContains( response, task.description)
            
        
    def testCreateInterface(self):
        """Test if you can create a tasks through the create view"""
        # given:
        self.description="afeitar el gato"
        self.initial_count = Task.objects.count()
        # when:
        request = RequestFactory().post(reverse('tasklist:task_create'), data={'description': self.description})
        response = TaskCreateView.as_view()(request)
        # then:
        self.final_count = Task.objects.count()
        task = Task.objects.get(description = self.description)
        self.assertEquals(response.status_code, 302, 'Status code should be 302 as it redirects to list view')
        self.assertEqual(self.initial_count+1, self.final_count, 'Number of tasks should be incremented by 1')
        self.assertEqual(task.description, self.description, 'The task should be stored in the DB')
        
    def testDeleteInterface(self):
        """Test if you can delete a task from the task list"""
        # given:
        self.description="afeitar el gato"
        task_list = [
            Task(description = self.description+' 1'),
            Task(description = self.description+' 2'),
            Task(description = self.description+' 3'),
        ]
        for task in task_list:
            task.save()
        self.initial_count = Task.objects.count()
        
        # when:
        pk = Task.objects.latest('id').id
        url = reverse('tasklist:task_delete', kwargs = {'pk': pk})
        request = RequestFactory().post(url)
        response = TaskDeleteView.as_view()(request, pk=pk)
        self.final_count = Task.objects.count()
        # then:
        self.assertEquals(response.status_code, 302, 'Status code should be 302 as it redirects to list view')
        self.assertEqual(self.initial_count-1, self.final_count, 'Number of tasks should be decreased by 1')
        self.assertTrue(not Task.objects.filter(pk=pk).exists())
        
    def testEditInterface(self):
        """Test if you can edit a task from the task list"""
        #given
        self.description="afeitar el gato"
        task_list = [
            Task(description = self.description+' 1'),
            Task(description = self.description+' 2'),
            Task(description = self.description+' 3'),
        ]
        for task in task_list:
            task.save()
        #when
        pk = Task.objects.latest('id').id
        url = reverse('tasklist:task_edit', kwargs = {'pk':pk})
        request = RequestFactory().post(url, data={'description': self.description})
        response = TaskUpdateView.as_view()(request, pk=pk)
        #then
        self.assertEquals(response.status_code, 302, 'Status code should be 302 as it redirects to list view')
        edited_task = Task.objects.get(pk = pk)
        self.assertEqual(edited_task.description, self.description, 'The description did not change')
        
    def testEditCompleteInterface(self):
        """Test if you can complete a task from the task list"""
        #given
        self.description="afeitar el gato"
        task_list = [
            Task(description = self.description+' 1'),
            Task(description = self.description+' 2'),
            Task(description = self.description+' 3'),
        ]
        for task in task_list:
            task.save()
        #when
        pk = Task.objects.latest('id').id
        url = reverse('tasklist:task_edit', kwargs = {'pk':pk})
        request = RequestFactory().post(url, data={'complete': True})
        response = TaskUpdateView.as_view()(request, pk=pk)
        #then
        self.assertEquals(response.status_code, 302, 'Status code should be 302 as it redirects to list view')
        edited_task = Task.objects.get(pk = pk)
        self.assertEqual(edited_task.complete, True, 'The complete status did not change')
        
        