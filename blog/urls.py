from django.urls import path
from . import views

# app_name = 'blog'

urlpatterns = [
    path('', views.main, name='main'),
    path('login', views.login, name='login'),
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

    path('employee_report/', views.employee_report, name = 'employee_report'),
    
    
    path('teacher_home/',views.teacher_home, name='teacher_home'),
    path('teacher_manage',views.teacher_manage,name='teacher_manage'),


    # Approve Student
    path('approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('disapprove-student/<int:student_id>/', views.disapprove_student, name='disapprove_student'),
    
    # Instructor
    path('instructor-home/', views.teacher_home, name='teacher_home'),
    path('instructor-manage/', views.teacher_manage, name='teacher_manage'),
    # path('section/', views.section, name='section'),
    path('student-dashboard/', views.section, name='section'),
    path('delete-section/<int:section_id>/', views.delete_section, name='delete_section'),

    # Send reqeust
    path('send-request/<int:id>/', views.send_request, name='send_request'),

    # Success
    path('success-teacher-approve/<uid>/<token>/', views.success_teacher_approval, name='success_teacher_approval'),
    path('success-employee-approve/<uid>/<token>/', views.success_employee_approval, name='success_employee_approval'),

    # Dashboard
    path('view-student-dashboard/<int:id>/', views.view_student_dashboard, name='view_student_dashboard'),
    path('view-employee-student-dashboard/<int:id>/', views.view_employee_student_dashboard, name='view_employee_student_dashboard'),

    # Submittion of reports
    path('submit-report/', views.submit_report, name='submit_report'),

    # Approval of reports
    path('approve-student-task/<int:student_id>/<int:id>/', views.approve_student_task, name='approve_student_task'),
    path('disapprove-student-task/<int:student_id>/<int:id>/', views.disapprove_student_task, name='disapprove_student_task'),
    path('approve-student-all/<int:id>/', views.approve_student_all, name='approve_student_all'),

    # ADMIN
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('confirmation-success/<uid>/<token>/', views.confirmation_success_employee, name='confirmation_success_employee'),

]






