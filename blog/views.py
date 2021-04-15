from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages

from datetime import datetime, date

from .models import Destination, TaskList, TaskType
from accounts.models import CustomUser

from .forms import ListForm



def login(request):
    if request.method =='POST':
        username = request.POST['username']
        
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_student:

                auth.login(request,user)
                print('login successfully')
                return redirect('home')
            else:
                messages.info(request,'invalid credentials')
                return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/')
    else:
        return render(request, 'blog/login.html')
    
def logindean(request):
    if request.method =='POST':
        username = request.POST['username']
        
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            print(user.is_teacher)
            if user.is_teacher:
                print(user.is_teacher)
                auth.login(request,user)
                print('login successfully')
                return redirect('/instructor-home')
            else:
                messages.info(request,'invalid credentials')
                return redirect('/logindean')
        else:
            messages.info(request,'invalid credentials')
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

                auth.login(request,user)
                print('login successfully')
                return redirect('/employee-home')
            else:
                messages.info(request,'invalid credentials')
                return redirect('/loginemployer')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/loginemployer')
    else:
        return render(request, 'blog/loginemployer.html')

def registration_student(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        employee_email = request.POST['employee_email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']

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
                        user = CustomUser.objects.create_user(
                            username=email, 
                            password=password1, 
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            my_employee=employee    
                        )
                        user.is_student = True
                        user.save()

                        employee.employer_student.add(user)
                        messages.info(request,'User Created!')

                        return redirect('/')
                    else:
                        messages.info(request,'Invalid employer email')
                        return redirect('registration_student')
        else:
            messages.info(request,'Password not matching!')
        return redirect('registration_student')
    else:
        return render(request, 'blog/registration_student.html')

def registration_dean(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        password1= request.POST['password1']    
        password2= request.POST['password2']
        email= request.POST['email']
        phone = request.POST['phone']
        question = request.POST['question']
        answer = request.POST['answer']
        gender = request.POST['gender']

        if password1==password2:
            if CustomUser.objects.filter(username=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_dean')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_dean')
            else:
                is_male = False
                if gender == 'male':
                    is_male = True

                user = CustomUser.objects.create_user(
                    username=email, 
                    password=password1, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    question=question,
                    answer=answer,
                    is_male=is_male
                )
                user.is_teacher = True
                user.save()
                messages.info(request,'User Created!')
                return redirect('/')
        else:
            messages.info(request,'Password not matching!')
        return redirect('registration_dean')
    else:
        return render(request, 'blog/registration_dean.html')

def registration_employer(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']
        phone = request.POST['phone']
        question = request.POST['question']
        answer = request.POST['answer']
        gender = request.POST['gender']

        if password1 == password2:
            if CustomUser.objects.filter(username=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_employer')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_employer')
            else:
                is_male = False
                if gender == 'male':
                    is_male = True

                employer = CustomUser.objects.create_user(
                    username=email, 
                    password=password1, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    question=question,
                    answer=answer,
                    is_male=is_male
                )
                employer.is_employee = True
                employer.save()
                messages.info(request,'User Created!')
                
                return redirect('/')
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
        task_list = TaskList.objects.filter(user=user)
        
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

        print(hours)
        print(essential)
        print(non_essential)

        print(essential_hour)
        print(non_essential_hour)

        return render(request,'blog/home.html', {
            'total_hour': hours,
            'essential': essential,
            'non_essential': non_essential,
            'essential_hour': essential_hour,
            'non_essential_hour': non_essential_hour
        })
    else:
        if request.user.is_teacher:
            return redirect('instructor-home/')
        
        if request.user.is_employee:
            return redirect('employee-home/')

@login_required
def task(request):

    if request.user.is_student:

        task_type = [
            'Essential',
            'Non-Essential'
        ]

<<<<<<< HEAD
    return render(request,'blog/home.html', {
        'total_hour': hours,
        'essential': essential,
        'non_essential': non_essential,
        'essential_hour': essential_hour,
        'non_essential_hour': non_essential_hour
    })
    

=======
        error = 'Invalid Date'
>>>>>>> 6f8f0cb156bcb0a6100f392a9e3a3e0f535538c3

        username = request.user.username
        user = CustomUser.objects.get(username=username)
        task_list = TaskList.objects.filter(user=user)

        if request.method =='POST':     
            # if request.POST['start_time'] < request.POST['end_time']:
            #     return render(request, 'blog/about.html', {
            #         'task_list':task_list,
            #         'task_type': task_type,
            #     })
            # else:
            #     return render(request, 'blog/about.html', {
            #         'task_list':task_list,
            #         'task_type': task_type,
            #     })

            task = TaskList.objects.create(
                user=user,
                start_time=request.POST['start_time'],
                task=request.POST['task'],
                end_time=request.POST['end_time'],
                task_type=request.POST['task_type']
            )

            return redirect('/task')

            # print(request.POST)
            # forms = ListForm(request.POST)
            # if forms.is_valid():
            #     forms.save()

            #     return redirect('/task')
                
        else:
            
            # form = ListForm()
            
            return render(request, 'blog/about.html', {
                # 'form':form, 
                'task_list':task_list,
                'task_type': task_type,
            })
    else:
        if request.user.is_teacher:
            return redirect('instructor-home/')
        
        if request.user.is_employee:
            return redirect('employee-home/')
    
    
    

    


def delete_list_item(request,list_id):
    list_to_delete=TaskList.objects.get(pk=list_id)
    list_to_delete.delete()
    return redirect('/task')

def logout(request):
    auth.logout(request)
    return redirect('/')

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
    

# Employer
@login_required
def teacher_home(request):

    if request.user.is_teacher:

        if request.method == 'GET':
            username = request.user.username

            # user = CustomUser.objects.get(username=username)
            # print(user.employee_students)
            return render(request, 'blog/teacher_home.html')
    else:
        if request.user.is_employee:
            return redirect('/employee-home')
        
<<<<<<< HEAD
        context = {
            'students': students
        }
        return render(
            request, 
            'blog/employee_pending.html',
            context
        )
        
@login_required
def employee_report(request): #Pending approval ng report summary
    if request.method == 'GET':
        username = request.user.username

        user = CustomUser.objects.get(username=username)
        students = user.employer_student.all()
        
        
        return render(
            request, 
            'blog/employee_report.html',
          
        )
        
        
#Teacher
def teacher_home(request):
    return render(request,'blog/teacher_home.html')

def teacher_manage(request):
    return render(request,'blog/teacher_manage.html')

=======
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

def send_request(request):
    user = request.user.username
    if request.method == 'POST':
        print(request.POST)
        student_id = request.POST['student']
        try:
            student = CustomUser.objects.get(id=student_id)
        except CustomUser.DoesNotExist:
            return redirect('/instructor-manage')
        else:
            teacher = CustomUser.objects.get(username=user)
            student.my_teacher = teacher
            student.pending_teacher = True
            student.save()
            return redirect('/instructor-manage')
>>>>>>> 6f8f0cb156bcb0a6100f392a9e3a3e0f535538c3
