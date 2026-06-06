from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Task


# ======================
# REGISTER
# ======================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# ======================
# LOGIN
# ======================
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Username atau password salah'
            })

    return render(request, 'login.html')


# ======================
# LOGOUT
# ======================
def logout_view(request):
    logout(request)
    return redirect('login')


# ======================
# DASHBOARD
# ======================
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Done').count()

    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    })


# ======================
# CREATE TASK
# ======================
@login_required
def create_task(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description']
        )
        return redirect('dashboard')

    return render(request, 'create_task.html')


# ======================
# UPDATE TASK
# ======================
@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.status = request.POST['status']
        task.save()
        return redirect('dashboard')

    return render(request, 'update_task.html', {'task': task})


# ======================
# DELETE TASK
# ======================
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    return render(request, 'delete_task.html', {'task': task})