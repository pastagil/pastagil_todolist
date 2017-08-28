from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from .models import Task
from .views import TaskListView, TaskCreateView, TaskDeleteView
from random import shuffle

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


class TaskInterfaceTest(TestCase):
    
    
    def testListInterfaceOld(self):
        """Test if you can get a task through the list view"""
        # given:
        self.description="afeitar el gato"
        task = Task.objects.create(description=self.description)
        client = Client()
        # when:
        response = client.get(reverse('tasklist:task_list'))
        # then:
        self.assertContains( response, self.description, status_code=200 )
        
    
    def testListInterface(self):
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
            
        