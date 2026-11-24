from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import *
from random import randint
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

def registraion(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )
        user.save()
        
        code = str(randint(100000, 999999))
        EmailConfirm.objects.update_or_create(user = user, code = code)
        send_mail(
            "Confirm your email",
            f"Your code {code}",
            'norep1y@softc1ub.tj',
            [user.email]
        )
        return redirect('confirm_email')
    
    return render(request, "registration.html")


def confirm_email(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        code = request.POST.get('code')
        user = User.objects.filter(username=username).first()
        if user:
            code_obj = EmailConfirm.objects.filter(user=user).first()
            if code_obj.code == code:
                user.is_active = True
                user.save()
                code_obj.delete()
                login(request, user)
                return redirect('profile')
        return redirect('confirm_email')
    return render(request, 'confirm_email.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('profile')

        return redirect('login')

    return render(request, 'login.html')


@login_required
def show_profile(request):
    return render(request, 'profile.html')


@login_required
def show_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        if title:
            Task.objects.create(user=request.user, title=title, description=description, due_date=due_date)
        return redirect('tasks')
    return render(request, 'create_task.html')


@login_required
def edit_task(request, id):
    task = Task.objects.filter(id=id, user=request.user).first()
    if not task:
        return redirect('tasks')
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.save()
        return redirect('tasks')
    return render(request, 'edit_task.html', {'task': task})


@login_required
def delete_task(request, id):
    task = Task.objects.filter(id=id, user=request.user).first()
    
    if request.method == 'POST':
        task.delete()
        
    return redirect('tasks')


@login_required
def change_status(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        status = request.POST.get('status')

        if status in ['new', 'in_progress', 'completed']:
            task.status = status
            task.save()

    return redirect('tasks')


@login_required
def chat(request):
    messages = Message.objects.all().order_by('created_at')
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(user=request.user, text=text)
        return redirect('chat')
    return render(request, 'chat.html', {'messages': messages})


@login_required
def edit_message(request, id):
    message = get_object_or_404(Message, id=id, user=request.user)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            message.text = text
            message.save()
            return redirect('chat')

    return render(request, 'edit_message.html', {'message': message})


@login_required
def delete_message(request, id):
    message = get_object_or_404(Message, id=id)
    if request.method == 'POST' and message.user == request.user:
        message.delete()
    return redirect('chat')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')