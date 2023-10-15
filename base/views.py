from django.shortcuts import render

# Create your views here.

# Commented out this bcoz we'll be using class based view

# from django.http import HttpResponse

# def taskList(request):
#     return HttpResponse('To Do List')

from django.views.generic.list import ListView

from .models import Task

class TaskList(ListView):
    model = Task
