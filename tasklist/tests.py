from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import Task
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
    
    
    def testInterface(self):
        # given:
        self.description="afeitar el gato"
        task = Task.objects.create(description=self.description)
        client = Client()
        # when:
        response = client.get(reverse('tasklist:task_list'))
        # then:
        # self.assertEquals(response.status_code, 200)
        self.assertContains( response, self.description, status_code=200 )
        