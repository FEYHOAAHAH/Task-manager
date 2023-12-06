from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks_todo = Task.objects.filter(status='todo').order_by('deadline', '-priority')
    tasks_done = Task.objects.filter(status='done').order_by('-priority')

    return render(request, 'task_list.html', {'tasks_todo': tasks_todo, 'tasks_done': tasks_done})


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})


def mark_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.status = 'done'
    task.save()
    return redirect('task_list')


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('task_list')
