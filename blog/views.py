from django.shortcuts import render, redirect
from .models import Destination, List
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import ListForm

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            print('login successfully')
            return redirect('home')
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
        
        if user is not None:
            auth.login(request,user)
            print('login successfully')
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/')
    else:
        return render(request, 'blog/logindean.html')
def loginemployer(request):
    if request.method =='POST':
        username = request.POST['username']
        
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            print('login successfully')
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/')
    else:
        return render(request, 'blog/loginemployer.html')

def registration_student(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        username= request.POST['username']
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('registration_student')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('registration_student')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request,'User Created!')
                return redirect('/')
        else:
            messages.info(request,'Password not matching!')
        return redirect('registration_student')
    else:
        return render(request, 'blog/registration_student.html')

def registration_dean(request):
    return render(request, 'blog/registration_dean.html')

def registration_employer(request):
    return render(request, 'blog/registration_employer.html')

def home(request):
#HELLO HAGAGAGAGAFDSFAWTWDASAFA
    
    return render(request,'blog/home.html')

def task(request):
    # title= {
    #     'title':'About'
    # }
    if request.method =='POST':
        forms = ListForm(request.POST)
        if forms.is_valid():
           forms.save()
           print('COMPLETED NICE ONE')
            
        return redirect('/task')
        
    else:
        
        print('Completed')
        viewlist = List.objects.all()
        form = ListForm()
        
        return render(request, 'blog/about.html', {'form':form, 'viewlist':viewlist})
    
def delete_list_item(request,list_id):
    list_to_delete=List.objects.get(pk=list_id)
    list_to_delete.delete()
    return redirect('/task')

def logout(request):
    auth.logout(request)
    return redirect('/')