from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', registraion, name='registration'),
    path('confirm/', confirm_email, name='confirm_email'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', show_profile, name='profile'),
    path('change-status/<int:id>/', change_status, name='change_status'),
    path('tasks/', show_tasks, name='tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/edit/<int:id>/', edit_task, name='edit_task'),
    path('tasks/delete/<int:id>/', delete_task, name='delete_task'),
    path('tasks/status/<int:id>/', change_status, name='change_status'),
    path('chat/', chat, name='chat'),
    path('delete-message/<int:id>/', delete_message, name='delete_message'),
    path('chat/edit/<int:id>/', edit_message, name='edit_message'),
]
