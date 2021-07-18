from os import error, pipe
from django.shortcuts import redirect, render
from .models import*
from django.contrib.auth.models import User    
from django.contrib.auth import authenticate, login,logout
from datetime import date
# Create your views here.

def index(request):
    return render(request, 'index.html')


#---login functions----

def admin_login(request):
    error=''
    if request.method=='POST':
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        user=authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                login(request,user)
                error='no'
            else:
                error='yes'
        except:
            error='yes'
    context={'error':error}

    return render(request, 'admin_login.html',context)


def user_login(request):
    error=''
    if request.method=='POST':
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        user=authenticate(username=uname, password=pwd)

        if user:
            try:
                user1=StudentUser.objects.get(user=user)
                if user1.type=='student':
                    login(request,user)
                    error='no'
                else:
                    error='yes'
            except:
                error='yes'
        else:
            error='yes'
    context={'error':error}
    return render(request, 'user_login.html',context)

def recruiter_login(request):
    error=''
    if request.method=='POST':
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        user=authenticate(username=uname, password=pwd)

        if user:
            try:
                user1=Recruiter.objects.get(user=user)
                if user1.type=='recruiter' and user1.status!='pending':
                    login(request,user)
                    error='no'
                else:
                    error='not'
            except:
                error='yes'
        else:
            error='yes'
    context={'error':error}
    return render(request, 'recruiter_login.html',context)

#--- Signup functions----

def user_signup(request):
    error=''
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        img=request.FILES['image']
        p=request.POST['pwd']
        c=request.POST['contact']
        email=request.POST['email']
        g=request.POST['gender']

        try:
            user=User.objects.create_user(first_name=f, last_name=l, username=email, password=p)
            StudentUser.objects.create(user=user, mobile=c, gender=g, image=img, type='student')
            error='no'
        except:
            error='yes'
        
    context={'error':error}
    return render(request, 'user_signup.html',context)

def recruiter_signup(request):
    error=''
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        img=request.FILES['image']
        p=request.POST['pwd']
        c=request.POST['contact']
        email=request.POST['email']
        g=request.POST['gender']
        company=request.POST['company']

        try:
            user=User.objects.create_user(first_name=f, last_name=l, username=email, password=p)
            Recruiter.objects.create(user=user, mobile=c, gender=g, image=img, company=company, type='recruiter', status='pending')
            error='no'
        except:
            error='yes'
        
    context={'error':error}
    return render(request, 'recruiter_signup.html',context)

#---home functions----

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    error=''
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        c=request.POST['contact']
        g=request.POST['gender']

        student.user.first_name=f
        student.user.last_name=l
        student.mobile=c
        student.gender=g

        try:
            student.save()
            student.user.save()
            error='no'
        except:
            error='yes'
        try:
            img=request.FILES['image']
            student.image=img
            student.save()
        except:
            pass
    data={'student':student,'error':error}
        
    return render(request, 'user_home.html',data)

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    error=''
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        c=request.POST['contact']
        g=request.POST['gender']
        company=request.POST['company']

        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=c
        recruiter.gender=g
        recruiter.company=company

        try:
            recruiter.save()
            recruiter.user.save()
            error='no'
        except:
            error='yes'
        try:
            img=request.FILES['image']
            recruiter.image=img
            recruiter.save()
        except:
            pass



    data={'recruiter':recruiter,'error':error}
    return render(request, 'recruiter_home.html',data)


#---logout functions----

def Logout(requset):
    logout(requset)
    return redirect('index')


def view_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    context={'data':data}
    return render(request, 'view_user.html',context)

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='pending')
    context={'data':data}
    return render(request, 'recruiter_pending.html',context)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Accept')
    context={'data':data}
    return render(request, 'recruiter_accepted.html',context)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Reject')
    context={'data':data}
    return render(request, 'recruiter_rejected.html',context)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    context={'data':data}
    return render(request, 'recruiter_all.html',context)

#---delete--------

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=User.objects.get(id=pid)
    student.delete()
    return redirect('view_user')

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=User.objects.get(id=pid)
    data.delete()
    return redirect('recruiter_all')

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=''
    data=Recruiter.objects.get(id=pid)
    if request.method=='POST':
        s=request.POST['status']
        data.status=s
        try:
            data.save()
            error='no'
        except:
            error='yes'
    context={'data':data,
              'error':error
            }
    return render(request, 'change_status.html',context)


#-----change password-----

def admin_change_pwd(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=''
   
    if request.method=='POST':
        old=request.POST['currentpwd']
        new=request.POST['newpwd']
       
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(old):
                u.set_password(new)
                u.save()
                error='no'
            else:
                error='not'
        except:
            error='yes'
    context={
              'error':error
            }
    return render(request, 'admin_change_pwd.html',context)


def user_change_pwd(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=''
   
    if request.method=='POST':
        old=request.POST['currentpwd']
        new=request.POST['newpwd']
       
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(old):
                u.set_password(new)
                u.save()
                error='no'
            else:
                error='not'
        except:
            error='yes'
    context={
              'error':error
            }
    return render(request, 'user_change_pwd.html',context)


def recruiter_change_pwd(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=''
   
    if request.method=='POST':
        old=request.POST['currentpwd']
        new=request.POST['newpwd']
       
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(old):
                u.set_password(new)
                u.save()
                error='no'
            else:
                error='not'
        except:
            error='yes'
    context={
              'error':error
            }
    return render(request, 'recruiter_change_pwd.html',context)

#----job-------

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=''
    if request.method=='POST':
        title=request.POST['title']
        sdate=request.POST['sdate']
        edate=request.POST['edate']
        salary=request.POST['salary']
        logo=request.FILES['logo']
        exp=request.POST['exp']
        location=request.POST['location']
        skills=request.POST['skills']
        desc=request.POST['desc']
        user=request.user
        recruiter=Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter, start_date=sdate, end_date=edate, 
                title=title, salary=salary, image=logo, description=desc, experience=exp, location=location, skills=skills, creation_date=date.today())
            error='no'
        except:
            error='yes'
    context={'error':error}

    return render(request, 'add_job.html',context)

#----job list------

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    context={'job':job}
    return render(request, 'job_list.html',context)

#----latest job------

def latest_job(request):
    data=Job.objects.all().order_by('-start_date')
    context={'data':data}
    return render(request, 'latest_job.html',context)

def user_show_latest_job(request):
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)
    context={'job':job,'li':li}
    return render(request, 'user_show_latest_job.html',context)


def job_details(request,pid):
    job=Job.objects.get(id=pid)
    data={'job':job}
    return render(request, 'job_details.html',data)

def apply_for_job(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=''
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if date1>job.end_date:
        error='close'
    elif date1<job.start_date:
        error='not_open'
    else:
        if request.method=='POST':
            res=request.FILES['resume']
            Apply.objects.create(job=job,student=student,resume=res,applydate=date.today())
            error='ok'
    context={'error':error,'job':job}
    return render(request, 'apply_for_job.html',context)

#----Edit job-----

def edit_job(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=''
    job=Job.objects.get(id=pid)
    if request.method=='POST':
        title=request.POST['title']
        sdate=request.POST['sdate']
        edate=request.POST['edate']
        salary=request.POST['salary']
        logo=request.FILES['logo']
        exp=request.POST['exp']
        location=request.POST['location']
        skills=request.POST['skills']
        desc=request.POST['desc']
        
        job.title=title
        job.salery=salary
        job.experience=exp
        job.image=logo
        job.location=location
        job.skills=skills
        job.description=desc
        try:
            job.save()
            error='no'
        except:
            error='yes'
        if sdate:
            try:
                job.start_date=sdate
                job.save()
            except:
                pass
        if edate:
            try:
                job.end_date=edate
                job.save()
            except:
                pass
    context={'error':error,
              'job':job
            }

    return render(request, 'edit_job_details.html',context)