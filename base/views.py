from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render , redirect

# Create your views here.

## Commented out this bcoz we'll be using class based view

# from django.http import HttpResponse

# def taskList(request):
#     return HttpResponse('To Do List')

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

# Resctritc few pages for the user
# We want the user to see the LOGIN page if loggedOut not the task_list.html which is the url 5000port
from django.contrib.auth.mixins import LoginRequiredMixin

# Register User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task



class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__' 
    redirect_authenticated_user = True #if the user is authenticated they shouldn't be allowed on this page

    #success_url = reverse_lazy('tasks')
    #same but we defined customized function by own
    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks')

    # After successful registration logging in the user
    def form_valid(self , form):
        user = form.save()
        if user is not None:
            login(self.request , user)
        return super(RegisterPage , self).form_valid(form)
    
    # Making sure the logged in user can't access the register page again
    def get(self , *args , **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage , self).get(*args , **kwargs)


# looks for task_list.html
class TaskList(LoginRequiredMixin , ListView):
    model = Task
    # setting context object name for task_list.html
    context_object_name = 'tasks'


    # The data of a particular user is visible to only that partcular user not to everyone
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        # context['color'] = 'red'
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count() # we just want to know the count of incomplete items

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        return context

# looks for task_detail.html
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html' #we changed task_detail.htm to task.html


# Creating tasks imported reverse lazy too for this one
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # fields = '__all__' #ModelForm
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')

    # Fixing user dropdown (selection) MAKING IT DEFAULT
    def form_valid(self , form):
        form.instance.user = self.request.user
        return super(TaskCreate , self).form_valid(form)

# Update Task imported UpdateView
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    # fields = '__all__' #ModelForm 
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')

# Delete Task imported DeleteView
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')