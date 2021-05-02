import datetime as dt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages

from datetime import datetime, date

from .models import Destination, TaskList, TaskType, Section
from accounts.models import CustomUser

from .forms import ListForm

from .services.teacher_request import teacher_request, account_activation_token
from .services.employee_request import employee_request
from .services.send_employer_request import send_employer_request
# For email 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_student:
                if user.is_student_approve:
                    date_today = dt.date.today()

                    if user.day_login == None or user.previous_day == None:
                        user.day_login = datetime.now()
                        user.previous_day = datetime.now()
                    elif user.day_login < date_today:
                        user.is_send = False
                        day_login = user.day_login

                        user.previous_day = day_login
                        user.day_login = datetime.now()
                    
                    user.save()

                    auth.login(request,user)
                    return redirect('home')
                else:
                    messages.info(request,'You are still for approval.')
                    return redirect('/')
            else:
                messages.info(request,'Invalid credentials')
                return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/')
    else:
        return render(request, 'blog/login.html')
    
def logindean(request):
    if request.method =='POST':
        username = request.POST['username']
        
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_teacher:
                date_today = dt.date.today()

                if user.day_login == None or user.previous_day == None:
                    user.day_login = datetime.now()
                    user.previous_day = datetime.now()
                elif user.day_login < date_today:
                    user.is_send = False
                    day_login = user.day_login

                    user.previous_day = day_login
                    user.day_login = datetime.now()
                
                user.save()

                auth.login(request,user)
                return redirect('/student-dashboard')
            else:
                messages.info(request,'Invalid credentials')
                return redirect('/logindean')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/logindean')
    else:
        return render(request, 'blog/logindean.html')

def loginemployer(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            if user.is_employee:
                date_today = dt.date.today()
                if user.day_login == None or user.previous_day == None:
                    user.day_login = datetime.now()
                    user.previous_day = datetime.now()
                elif user.day_login < date_today:
                    user.is_send = False
                    user.is_switch = False
                    day_login = user.day_login

                    user.previous_day = day_login
                    user.day_login = datetime.now()

                user.save()

                auth.login(request,user)
                return redirect('/employee-home')
            else:
                messages.info(request,'Invalid credentials')
                return redirect('/loginemployer')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/loginemployer')
    else:
        return render(request, 'blog/login_employer.html')

def registration_student(request):

    schools = [
        'New Era Branch 1',
        'New Era Branch 2',
        'New Era Branch 3',
        'New Era Branch 4'
    ]

    context = {
        'schools': schools
    }

    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        employee_email = request.POST['employee_email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']
        section_code = request.POST['section_code']
        school_name = request.POST['school_name']

        if password1==password2:
            if CustomUser.objects.filter(username=email).exists():
                messages.info(request,'Username Taken')
                return redirect('registration_student')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_student')
            else:
                try:
                    employee = CustomUser.objects.get(email=employee_email)
                except CustomUser.DoesNotExist:
                    messages.info(request,'Invalid employer email')
                    return redirect('registration_student')
                else:
                    if employee.is_employee:
                        try:
                            section = Section.objects.get(section_code=section_code)
                        except Section.DoesNotExist:
                            messages.info(request,'Invalid Section Code!')
                            return redirect('registration_student')
                        else:
                            if section.school_name != school_name:
                                messages.info(request,'{} does not exsit in {}!'.format(section_code, school_name))
                                return redirect('registration_student')
                            else:
                                user = CustomUser.objects.create_user(
                                    username=email, 
                                    password=password1, 
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    my_employee=employee,
                                    school_name=school_name,
                                    section_code=section_code
                                )
                                user.is_student = True
                                user.save()

                                employee.employer_student.add(user)

                                employee_request(    
                                    email_to=employee.email,
                                    name=employee.first_name.title(),
                                    user_pk=user.pk,
                                    user=user,
                                    student_email=email
                                )

                                section.students.add(user)

                                messages.info(request,'User Created!')

                                return redirect('/')
                    else:
                        messages.info(request,'Invalid employer email')
                        return redirect('registration_student')
        else:
            messages.info(request,'Password not matching!')
        return redirect('registration_student')
    else:
        return render(request, 'blog/registration_student.html', context)

def registration_dean(request):
    schools = [
        'New Era Branch 1',
        'New Era Branch 2',
        'New Era Branch 3',
        'New Era Branch 4'
    ]

    context = {
        'schools': schools
    }

    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        password1= request.POST['password1']    
        password2= request.POST['password2']
        email= request.POST['email']
        school_name = request.POST['school_name']
        # phone = request.POST['phone']
        # question = request.POST['question']
        # answer = request.POST['answer']
        # gender = request.POST['gender']

        if password1==password2:
            if CustomUser.objects.filter(username=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_dean')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_dean')
            else:
            #     is_male = False
            #     if gender == 'male':
            #         is_male = True

                user = CustomUser.objects.create_user(
                    username=email, 
                    password=password1, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name,
                    school_name=school_name
                    # phone=phone,
                    # question=question,
                    # answer=answer,
                    # is_male=is_male
                )
                user.is_teacher = True
                user.save()
                messages.info(request,'User Created!')
                return redirect('/')
        else:
            messages.info(request,'Password not matching!')
        return redirect('registration_dean')
    else:
        return render(request, 'blog/registration_dean.html', context)

def registration_employer(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']
        username = request.POST['username']

        # phone = request.POST['phone']
        # question = request.POST['question']
        # answer = request.POST['answer']
        # gender = request.POST['gender']

        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_employer')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_employer')
            else:
            #     is_male = False
            #     if gender == 'male':
            #         is_male = True

                employer = CustomUser.objects.create_user(
                    username=username, 
                    password=password1, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name,
                    # phone=phone,
                    # question=question,
                    # answer=answer,
                    # is_male=is_male
                )

                employer.is_employee = True
                employer.save()
                messages.info(request,'User Created!')
                
                return redirect('/admin-home')
        else:
            messages.info(request,'Password not matching!')
        return redirect('registration_employer')
    else:
        return render(request, 'blog/registration_employer.html')
    

def employer_dashboard(request):
    print('yes')
    return render(request, 'blog/employer_dashboard.html')

def employer_task(request):
    return render(request, 'blog/employer_task.html')

@login_required
def home(request):

    if request.user.is_student:
        user = CustomUser.objects.get(username=request.user.username)
        task_list = TaskList.objects.filter(
            user=user, is_employee_accepted=True)
        
        hours = 0
        essential = 0
        non_essential = 0
        essential_hour = 0
        non_essential_hour = 0

        for task in task_list:
            start_time = task.start_time
            end_time = task.end_time
    
            if end_time > start_time:
                time_spent = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
                total_time_spent = time_spent.total_seconds()

                hour = int(total_time_spent // 3600)
                hours += hour
                # minutes = int((total_time_spent % 3600) // 60)
                # seconds = int(total_time_spent % 60)

                if task.task_type == 'Essential':
                    essential += 1
                    essential_hour += hour
                elif task.task_type == 'Non-Essential':
                    non_essential += 1
                    non_essential_hour += hour

        # Latest Approved Task
        latest_task = TaskList.objects.filter(
            user=user, is_current=True, is_employee_accepted=True)

        latest_date = None
        latest_hours = 0
        latest_essential = 0
        latest_non_essential = 0
        latest_essential_hour = 0
        latest_non_essential_hour = 0
        
        print(latest_essential)
        print(latest_essential_hour)

        for task in latest_task:
            latest_date = task.date_created
            start_time = task.start_time
            end_time = task.end_time

            print(task)
            if end_time > start_time:
                time_spent = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
                total_time_spent = time_spent.total_seconds()

                hour = int(total_time_spent // 3600)
                latest_hours += hour


                print(task.task_type)
                if task.task_type == 'Essential':
                    latest_essential += 1
                    latest_essential_hour += hour

                elif task.task_type == 'Non-Essential':
                    latest_non_essential += 1
                    latest_non_essential_hour += hour

        return render(request,'blog/home.html', {
            'total_hour': hours,
            'essential': essential,
            'non_essential': non_essential,
            'essential_hour': essential_hour,
            'non_essential_hour': non_essential_hour,
            'latest_date': latest_date,
            'latest_hour': latest_hours,
            'latest_essential': latest_essential,
            'latest_non_essential': latest_non_essential,
            'latest_essential_hour': latest_essential_hour,
            'latest_non_essential_hour': latest_non_essential_hour
        })
    else:
        if request.user.is_teacher:
            return redirect('/instructor-home')
        
        if request.user.is_employee:
            return redirect('/employee-home')

@login_required
def task(request):

    if request.user.is_student:

        task_type = [
            'Essential',
            'Non-Essential'
        ]

        error = 'Invalid Date'

        username = request.user.username
        user = CustomUser.objects.get(username=username)

        task_list = TaskList.objects.filter(
            user=user, is_send=False, date_created=datetime.now())

        if request.method =='POST':     
            print(request.POST['start_time'])
            print(request.POST['end_time'])
            if request.POST['start_time'] < request.POST['end_time']:
                
                task = TaskList.objects.create(
                    user=user,
                    start_time=request.POST['start_time'],
                    task=request.POST['task'],
                    end_time=request.POST['end_time'],
                    task_type=request.POST['task_type']
                )

                return redirect('/task')
            else:
                print('Hereee')
                return render(request, 'blog/about.html', {
                    'task_list':task_list,
                    'task_type': task_type,
                })
            # else:
            #     return render(request, 'blog/about.html', {
            #         'task_list':task_list,
            #         'task_type': task_type,
            #     }
        else:
            return render(request, 'blog/about.html', {
                'task_list':task_list,
                'task_type': task_type,
            })
    else:
        if request.user.is_teacher:
            return redirect('instructor-home/')
        
        if request.user.is_employee:
            return redirect('employee-home/')

def submit_report(request):
    username = request.user.username
    user = CustomUser.objects.get(username=username)

    task_list = TaskList.objects.filter(
        user=user, is_send=False, date_created=datetime.now())

    for task in task_list:
        task.is_send = True
        task.save()

    user.is_send = True
    user.save()

    # current_switch = TaskList.objects.filter(
    #     user=user, is_current=True, is_employee_accepted=True
    # )

    # for current in current_switch:
    #     current.is_current = False
    #     current.save()

    return redirect('/task')

def delete_list_item(request,list_id):
    list_to_delete=TaskList.objects.get(pk=list_id)
    list_to_delete.delete()
    return redirect('/task')

def logout(request):
    if request.user.is_student:
        auth.logout(request)
        return redirect('/')
    if request.user.is_teacher:
        auth.logout(request)
        return redirect('/logindean')
    if request.user.is_employee:
        auth.logout(request)
        return redirect('/loginemployer')

# Employer
@login_required
def employee_home(request):
    if request.user.is_employee:
        if request.method == 'GET':
            username = request.user.username

            user = CustomUser.objects.get(username=username)
            students = user.employer_student.all()

            context = {
                'students': students
            }

            return render(
                request, 
                'blog/employee_home.html',
                context
            )
    else:
        if request.user.is_teacher:
            return redirect('/instructor-home')
        
        if request.user.is_student:
            return redirect('/home')

@login_required
def employee_pending(request):
    if request.user.is_employee:
        if request.method == 'GET':
            username = request.user.username

            user = CustomUser.objects.get(username=username)
            students = user.employer_student.all()
            
            context = {
                'students': students
            }
            return render(
                request, 
                'blog/employee_pending.html',
                context
            )
    else:
        if request.user.is_teacher:
            return redirect('/instructor-home')
        
        if request.user.is_student:
            return redirect('/home')

def approve_student(request ,student_id):
    try:
        student = CustomUser.objects.get(id=student_id)
    except CustomUser.DoesNotExist:
        return redirect('/employee-pending')
    else:
        student.is_student_approve = True
        student.save()
        return redirect('/employee-pending')
        
@login_required
def employee_report(request): #Pending approval ng report summary
    if request.method == 'GET':
        username = request.user.username

        user = CustomUser.objects.get(username=username)
        students = user.employer_student.all()

        student_reports = list()

        for student in students:
            task = TaskList.objects.filter(
                user=student, 
                is_send=True, 
                is_employee_accepted=False
            )

            student_reports.append({
                'student': student,
                'reports': task
            })

        context = {
            'students': students,
            'student_reports': student_reports
        }
        
        return render(
            request, 
            'blog/employee_report.html',
            context
        )

def approve_student_task(request, student_id, id):
    username = request.user.username
    employee = CustomUser.objects.get(username=username)
    user = CustomUser.objects.get(id=student_id)

    date_today = dt.date.today()
    if date_today > user.previous_day and user.is_switch == False:
        current_switch = TaskList.objects.filter(
            user=user, is_current=True, is_employee_accepted=True
        )

        user.is_switch = True
        user.save()
        for current in current_switch:
            current.is_current = False
            current.save()


    task = TaskList.objects.get(id=id)
    task.is_current = True
    task.is_employee_accepted = True
    task.save()

    return redirect('/employee_report')

def approve_student_all(request, id):
    username = request.user.username
    user = CustomUser.objects.get(username=username)
    student = CustomUser.objects.get(id=id)

    date_today = dt.date.today()
    if date_today > user.previous_day and user.is_switch == False:
        current_switch = TaskList.objects.filter(
            user=student, is_current=True, is_employee_accepted=True
        )

        user.is_switch = True
        user.save()
        for current in current_switch:
            current.is_current = False
            current.save()

    tasks = TaskList.objects.filter(
        user=student, 
        is_send=True, 
        is_employee_accepted=False
    )

    for task in tasks:
        task.is_current = True
        task.is_employee_accepted = True
        task.save()

    return redirect('/employee_report')



# Employer
@login_required
def teacher_home(request):
    if request.user.is_teacher:
        if request.method == 'GET':
            username = request.user.username
            user = CustomUser.objects.get(username=username)
            students = user.teacher_students.all()
            context = {
                'students': students
            }
            return render(
                request, 
                'blog/teacher_home.html',
                context
            )
    else:
        if request.user.is_employee:
            return redirect('/employee-home')
        
        if request.user.is_student:
            return redirect('/home')

@login_required
def teacher_manage(request):
    if request.user.is_teacher:
        if request.method == 'GET':
            username = request.user.username
            
            students = CustomUser.objects.filter(
                is_student=True, accept_teacher=False, pending_teacher=False)
            # user = CustomUser.objects.get(username=username)
            # students = user.employer_student.all()
            
            context = {
                'students': students
            }
            return render(
                request, 
                'blog/teacher_manage.html',
                context
            )
    else:
        if request.user.is_employee:
            return redirect('/employee-home')
        
        if request.user.is_student:
            return redirect('/home')

def send_request(request, id):
    user = request.user.username
    if request.method == 'POST':
        student_id = id
        try:
            student = CustomUser.objects.get(id=student_id)
        except CustomUser.DoesNotExist:
            return redirect('/instructor-manage')
        else:
            teacher = CustomUser.objects.get(username=user)
            student.my_teacher = teacher
            student.pending_teacher = True
            student.save()

            teacher_request(
                email_to=student.email,
                name=student.first_name.title(),
                user_pk=student.pk,
                user=student,
                instructor_name=user
            )

            return redirect('/instructor-manage')

def success_teacher_approval(request, uid, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid))
    except ValueError as e:
        return render(request, 'errors/teacher_approval_failed.html')
    else:
        try:
            user = CustomUser.objects.get(pk=uid)
        
        except ValueError as e:
            return render(request, 'errors/teacher_approval_failed.html')
        else:
            if user is not None and account_activation_token.check_token(user, token):
                user.accept_teacher = True
                user.save()
                
                teacher = CustomUser.objects.get(id=user.my_teacher.id)
                teacher.teacher_students.add(user)
                return render(request, 'success/teacher_approval_success.html')
            else:
                return render(request, 'errors/teacher_approval_failed.html')

            return redirect('/instructor-manage')

def success_employee_approval(request, uid, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid))
    except ValueError as e:
        return render(request, 'errors/employee_approval_failed.html')
    else:
        try:
            user = CustomUser.objects.get(pk=uid)
        
        except ValueError as e:
            return render(request, 'errors/employee_approval_failed.html')
        else:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_student_approve = True
                user.save()

                print('HEllo')
            
                return render(request, 'success/employee_approval_success.html')
            else:
                print('failed')
                return render(request, 'errors/employee_approval_failed.html')

            return redirect('/employee-home')

def view_student_dashboard(request, id):
    if request.method == 'POST':
        student_id = id
        student = CustomUser.objects.get(id=student_id)
        task_list = TaskList.objects.filter(
            user=student, is_employee_accepted=True
        )
        
        hours = 0
        essential = 0
        non_essential = 0

        essential_hour = 0
        non_essential_hour = 0
        for task in task_list:
            start_time = task.start_time
            end_time = task.end_time

    
            if end_time > start_time:
                time_spent = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
                total_time_spent = time_spent.total_seconds()

                hour = int(total_time_spent // 3600)
                hours += hour

                if task.task_type == 'Essential':
                    essential += 1
                    essential_hour += hour
                elif task.task_type == 'Non-Essential':
                    non_essential += 1
                    non_essential_hour += hour

        # Latest Approved Task
        latest_task = TaskList.objects.filter(
            user=student, is_current=True, is_employee_accepted=True)

        latest_date = None
        latest_hours = 0
        latest_essential = 0
        latest_non_essential = 0
        latest_essential_hour = 0
        latest_non_essential_hour = 0
        
        for task in latest_task:
            latest_date = task.date_created
            start_time = task.start_time
            end_time = task.end_time
    
            if end_time > start_time:
                time_spent = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
                total_time_spent = time_spent.total_seconds()

                hour = int(total_time_spent // 3600)
                latest_hours += hour

                if task.task_type == 'Essential':
                    latest_essential += 1
                    latest_essential_hour += hour

                elif task.task_type == 'Non-Essential':
                    latest_non_essential += 1
                    latest_non_essential_hour += hour


        context = {
            'student': student.first_name.title(),
            'total_hour': hours,
            'essential': essential,
            'non_essential': non_essential,
            'essential_hour': essential_hour,
            'non_essential_hour': non_essential_hour,
            'latest_date': latest_date,
            'latest_hour': latest_hours,
            'latest_essential': latest_essential,
            'latest_non_essential': latest_non_essential,
            'latest_essential_hour': latest_essential_hour,
            'latest_non_essential_hour': latest_non_essential_hour
        }
        return render(
            request, 
            'blog/student_teacher_dashboard.html',
            context
        )

def view_employee_student_dashboard(request, id):
    username = request.user.username

    user = CustomUser.objects.get(username=username)

    if user.is_employee:
        if request.method == 'POST':
            student_id = id
            student = CustomUser.objects.get(id=student_id)
            task_list = TaskList.objects.filter(
                user=student, is_employee_accepted=True)
            
            hours = 0
            essential = 0
            non_essential = 0

            essential_hour = 0
            non_essential_hour = 0
            for task in task_list:
                start_time = task.start_time
                end_time = task.end_time

        
                if end_time > start_time:
                    time_spent = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
                    total_time_spent = time_spent.total_seconds()

                    hour = int(total_time_spent // 3600)
                    hours += hour

                    if task.task_type == 'Essential':
                        essential += 1
                        essential_hour += hour
                    elif task.task_type == 'Non-Essential':
                        non_essential += 1
                        non_essential_hour += hour


            # Latest Approved Task
            latest_task = TaskList.objects.filter(
                user=student, is_current=True, is_employee_accepted=True)

            latest_date = None
            latest_hours = 0
            latest_essential = 0
            latest_non_essential = 0
            latest_essential_hour = 0
            latest_non_essential_hour = 0
            
            for task in latest_task:
                latest_date = task.date_created
                start_time = task.start_time
                end_time = task.end_time
        
                if end_time > start_time:
                    time_spent = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
                    total_time_spent = time_spent.total_seconds()

                    hour = int(total_time_spent // 3600)
                    latest_hours += hour

                    if task.task_type == 'Essential':
                        latest_essential += 1
                        latest_essential_hour += hour

                    elif task.task_type == 'Non-Essential':
                        latest_non_essential += 1
                        latest_non_essential_hour += hour

            context = {
                'student': student.first_name.title(),
                'total_hour': hours,
                'essential': essential,
                'non_essential': non_essential,
                'essential_hour': essential_hour,
                'non_essential_hour': non_essential_hour,
                'latest_date': latest_date,
                'latest_hour': latest_hours,
                'latest_essential': latest_essential,
                'latest_non_essential': latest_non_essential,
                'latest_essential_hour': latest_essential_hour,
                'latest_non_essential_hour': latest_non_essential_hour
            }
            return render(
                request, 
                'blog/student_employee_dashboard.html',
                context
            )

def section(request):
    username = request.user.username
    user = CustomUser.objects.get(username=username)

    if request.method == 'POST':
        section_name = request.POST['section_name']

        section = Section.objects.create(
            section_name=section_name,
            school_name=user.school_name
        )

        return redirect('/student-dashboard')
    elif request.method == 'GET':
        sections = Section.objects.filter(school_name=user.school_name)

        print(sections)
        for section in sections:
            print(section.students.all(

            ))
        context = {
            'sections': sections
        }
        return render(request, 'blog/section.html', context)

def delete_section(request, section_id):
    if request.method == 'POST':
        section = Section.objects.get(id=section_id)

        section.delete()

        return redirect('/student-dashboard')


def test(request):
    return render(request, 'services/employee_request.html')

def admin_panel(request):
    if request.method == 'GET':
        return render(request, 'blog/admin_land.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                auth.login(request,user)
                return redirect('/admin-home')
            else:
                messages.info(request,'Invalid admin account!')
                return redirect('/admin-panel')
        else:
            messages.info(request,'Invalid account credentials')
            return redirect('/admin-panel')

        return redirect('/admin-home')
       

@login_required(login_url='/admin-panel')
def admin_home(request):
    if request.method == 'GET':
        employees = CustomUser.objects.all()
        context = {
            'employees': employees
        }
        return render(request, 'blog/admin.html', context)
    elif request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']
        username = request.POST['username']

        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_employer')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_employer')
            else:
                employer = CustomUser.objects.create_user(
                    username=username, 
                    password=password1, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name,
                )

                employer.is_employee = True
                employer.save()

                is_success = send_employer_request(
                    email_to=email,
                    name=first_name.title(),
                    user_pk=employer.pk,
                    user=employer,
                    username=username,
                    password=password1
                )
  
                messages.info(request,'User Created!')
                
                return redirect('/admin-home')
        else:
            messages.info(request,'Password not matching!')
        return redirect('/admin-home')

def confirmation_success_employee(request, uid, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid))
    except ValueError as e:
        return render(request, 'errors/send_employer_request.html')
    else:
        try:
            user = CustomUser.objects.get(pk=uid)
        
        except ValueError as e:
            return render(request, 'errors/send_employer_request.html')
        else:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_confirm_employer = True
                user.save()
                return render(request, 'success/send_employer_request.html')
            else:
                return render(request, 'errors/send_employer_request.html')

            return redirect('/')

def admin_logout(request):
    auth.logout(request)
    return redirect('/admin-panel')

