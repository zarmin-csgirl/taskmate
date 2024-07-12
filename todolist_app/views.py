from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
#Create your views here.

@login_required()
def todolist(request):
     if request.method == 'POST':
          form = TaskForm(request.POST or None)
          if form.is_valid():
               instance = form.save(commit=False)
               instance.manage = request.user
               instance.save()
          messages.success(request, 'Your task has been saved.')
          return redirect('todolist')
     else:
          all_tasks = TaskList.objects.filter(manage=request.user)
          paginator = Paginator(all_tasks, 5)
          page = request.GET.get('pg')
          all_tasks = paginator.get_page(page)

          return render(request, 'todolist.html', {'all_tasks': all_tasks})

@login_required()
def delete_task(request, task_id):
     task = TaskList.objects.get(pk=task_id)
     if task.manage == request.user:
        task.delete()
     else:
         messages.error(request, ("Access Restricted, You Are Not Allowed!"))
     return redirect('todolist')

@login_required()
def complete_task(request, task_id):
     task = TaskList.objects.get(pk=task_id)
     if task.manage == request.user:
         task.done = True
         task.save()
     else:
         messages.error(request, ("Access Restricted, You Are Not Allowed!"))
     return redirect('todolist')

@login_required()
def pending_task(request, task_id):
     task = TaskList.objects.get(pk=task_id)
     task.done = False
     task.save()
     return redirect('todolist')

@login_required()
def edit_task(request, task_id):
    task = get_object_or_404(TaskList, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task Edited Successfully.')
            return redirect('tasklist')  # Adjust the redirection as necessary
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})

def index(request):
     context = {
          'about_text' : "Welcome to About Page!",
     }
     return render(request, 'index.html', context)

def contact(request):
     context = {
          'contact_text' : "Welcome to Contact Page!",
     }
     return render(request, 'contact.html', context)

def about(request):
     context = {
          'about_text' : "Welcome to About Page!",
     }
     return render(request, 'about.html', context)