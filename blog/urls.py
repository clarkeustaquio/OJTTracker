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

    
    # path()
    

    # Employer
    path('employee-home/', views.employee_home, name='employee_home'),
    path('employee-pending/', views.employee_pending, name='employee_pending'),
<<<<<<< HEAD
    path('employee_report/', views.employee_report, name = 'employee_report'),
    
    
    path('teacher_home/',views.teacher_home, name='teacher_home'),
    path('teacher_manage',views.teacher_manage,name='teacher_manage')
=======

    # Approve Student
    path('approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    
    # Instructor
    path('instructor-home/', views.teacher_home, name='teacher_home'),
    path('instructor-manage/', views.teacher_manage, name='teacher_manage'),

    # Send reqeust
    path('send-request/', views.send_request, name='send_request')
>>>>>>> 6f8f0cb156bcb0a6100f392a9e3a3e0f535538c3
]




