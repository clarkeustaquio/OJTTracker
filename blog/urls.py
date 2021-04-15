from django.urls import path
from . import views

# app_name = 'blog'

urlpatterns = [
    path('', views.login, name='login'),
    path('logindean', views.logindean, name ='logindean'),
    path('loginemployer', views.loginemployer, name='loginemployer'),
    path('registration_student', views.registration_student, name='registration_student'),
    path('registration_dean', views.registration_dean, name='registration_dean'),
    path('registration_employer', views.registration_employer, name='registration_employer'),
    path('home', views.home, name='home'),
    path('task', views.task, name='blog_about'),
    path('logout', views.logout, name ='logout'),
    path('delete_list/<int:list_id>/',views.delete_list_item, name='delete_list_item'),
    path('employer_dashboard',views.employer_dashboard, name='employer_dashboard'),
    path('employer_task',views.employer_task, name='employer_task')
    
    # path()
    
    
]




