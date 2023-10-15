from django.shortcuts import render

# Create your views here.

## Commented out this bcoz we'll be using class based view

# from django.http import HttpResponse

# def taskList(request):
#     return HttpResponse('To Do List')

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Task


# looks for task_list.html
class TaskList(ListView):
    model = Task
    # setting context object name for task_list.html
    context_object_name = 'tasks'

# looks for task_detail.html
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html' #we changed task_detail.htm to task.html