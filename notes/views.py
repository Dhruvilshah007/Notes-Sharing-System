from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date

# Main Navigation Bar
def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')


#ADMIN LOGIN

def login_admin(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"

        except:
            error="yes"
    d={'error':error}
    return render(request,'login_admin.html',d)

  


#ADMIN NAVIGATION BAR  

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    pn=Notes.objects.filter(status="pending").count()
    an=Notes.objects.filter(status="Accept").count()
    rn=Notes.objects.filter(status="Reject").count()
    alln=Notes.objects.all().count()
    d={'pn':pn,'an':an,'rn':rn,'alln':alln}
    return render(request,'admin_home.html',d)

def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.filter(status="pending")
    d={'notes':notes}
    return render(request,'pending_notes.html',d)

def accept_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.filter(status="Accept")
    d={'notes':notes}
    return render(request,'accept_notes.html',d)

def reject_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.filter(status="Reject")
    d={'notes':notes}
    return render(request,'reject_notes.html',d)

def view_allnotes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes=Notes.objects.all()
    d={'notes':notes}
    return render(request,'view_allnotes.html',d)

def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
 
    users=User.objects.get(id=pid)
    users.delete()
    return redirect('view_users')

def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
 
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('view_allnotes')

def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
 
    notes=Notes.objects.get(id=pid)
    error=""
    if request.method=="POST":
        s=request.POST['status']
        try:
            notes.status=s
            notes.save()
            error="no"
        except:
            error="yes"
    d={'error':error,'notes':notes}
    return render(request,'assign_status.html',d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users=Signup.objects.all()
    d={'users':users}
    return render(request,'view_users.html',d)




#USER LOGIN

def userlogin(request):
    error=""
    if request.method=='POST':
        u=request.POST['emailid']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user:
                login(request,user)
                error="no"
            else:
                error="yes"

        except:
            error="yes"
    d={'error':error}
    return render(request,'userlogin.html',d)

def signup1(request):
    error=""
    if request.method=='POST':
        f=request.POST['firstname']
        l=request.POST['lastname']
        c=request.POST['contact']
        e=request.POST['emailid']
        p=request.POST['password']
        b=request.POST['branch']
        r=request.POST['role']
        try:
            user=User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user,contact=c,branch=b,role=r)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'signup.html',d)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=user)

    d={'data':data,'user':user}

    return render(request,'profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error=""
    if request.method=="POST":
        o=request.POST['old']
        n=request.POST['new']
        c=request.POST['confirm']
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request,'changepassword.html',d)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=user)
    error=False
    if request.method=="POST":
        f=request.POST['firstname']
        l=request.POST['lastname']
        c=request.POST['contact']
        b=request.POST['branch']
        user.first_name=f
        user.last_name=l
        data.contact=c
        data.branch=b
        user.save()
        data.save()
        error=True
    d={'data':data,'user':user,'error':error}
    return render(request,'edit_profile.html',d)
 
def Logout(request):
    logout(request)
    return redirect('/')


#User  Navigation Bar

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error=""
    if request.method=='POST':
        b=request.POST['branch']
        s=request.POST['subject']
        n=request.FILES['notesfile']
        f=request.POST['filetype']
        d=request.POST['description']
        u=User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,filetype=f,description=d,status='pending')
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'upload_notes.html',d)

def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user=User.objects.get(id=request.user.id)
    notes=Notes.objects.filter(user=user)
    d={'notes':notes}
    return render(request,'view_mynotes.html',d)

def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
 
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('view_mynotes')

def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    notes=Notes.objects.filter(status="Accept")
    d={'notes':notes}
    return render(request,'viewallnotes.html',d)

