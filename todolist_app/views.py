from django.shortcuts import render , redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request , ("Task added! Complete it soon!"))
        return redirect('todolist')

    else:
        #all_tasks = TaskList.objects.all()
        all_tasks = TaskList.objects.filter(owner=request.user)
        paginator = Paginator(all_tasks,5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        
        return render(request , 'todolist.html' ,{'all_tasks' : all_tasks})

@login_required
def delete_task(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
         task.delete()
    else:
         messages.error(request , ("Access Restricted"))
    return redirect('todolist')

def index(request):
    context = {
        'index_text' : "Welcome to home page"
    }
    return render(request,'index.html',context)

@login_required
def change_status(request ,task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        if task.done:
            task.done = False
        else:
            task.done = True
        task.save()
    else :
        messages.error(request , ("Access Restricted"))
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method == "POST":
        task_to_update = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None , instance = task_to_update)
        if form.is_valid():
            form.save()
            messages.success(request , ("Task Edited!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request , 'edit.html' , {'task_obj' : task_obj})



def contact(request):
    context = {
        'contact_text' : "This is Contact Page ",
    }
    return render(request , 'contact.html' ,context)


def about(request):
    context = {
        'about_text' : "This is about page",
    }
    return render(request , 'about.html' ,context)