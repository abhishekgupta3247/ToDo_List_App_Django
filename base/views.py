from django.shortcuts import render

# Create your views here.

## Commented out this bcoz we'll be using class based view

# from django.http import HttpResponse

# def taskList(request):
#     return HttpResponse('To Do List')

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

# Resctritc few pages for the user
# We want the user to see the LOGIN page if loggedOut not the task_list.html which is the url 5000port
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task



class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__' 
    redirect_authenticated_user = True #if the user is authenticated they shouldn't be allowed on this page

    #success_url = reverse_lazy('tasks')
    #same but we defined customized function by own
    def get_success_url(self):
        return reverse_lazy('tasks')


# looks for task_list.html
class TaskList(LoginRequiredMixin , ListView):
    model = Task
    # setting context object name for task_list.html
    context_object_name = 'tasks'

# looks for task_detail.html
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html' #we changed task_detail.htm to task.html

# Creating tasks imported reverse lazy too for this one
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = '__all__' #ModelForm
    success_url = reverse_lazy('tasks')


# Update Task imported UpdateView
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__' #ModelForm 
    success_url = reverse_lazy('tasks')

# Delete Task imported DeleteView
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')