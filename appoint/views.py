from django.shortcuts import render,redirect

# Create your views here.



def login(request,des):
    if request.method=='POST':
      username=request.POST['username']
      password=request.POST['password']
      print(username)
      print(password)
      if(des == 'patient'):
          user = auth.authenticate(username=username,password=password)
          if (user is not None) and (user.is_patient == True):
              auth.login(request,user)
              return redirect('/')
          else:
              messages.info(request,'Credentials not matched')
              return redirect('login',des)
      elif(des == 'doctor'):
          user = auth.authenticate(username=username,password=password)
          if (user is not None) and (user.is_doctor == True):
              auth.login(request,user)
              return redirect('/')
          else:
              messages.info(request,'Credentials not matched')
              return redirect('login',des)  
      
      else:
          messages.info(request,'Credentials not matched')
          return redirect('login',des)
    else:
      return render(request,'login.html')
   


def register(request,des):
    submitted =False
    if(request.method=='POST'):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']    
        
        if password1==password2 :
         if User.objects.filter(username=username).exists():
            messages.info(request,'Username is taken')
            return redirect('register',des)
         elif User.objects.filter(email=email).exists():
            messages.info(request,'email is taken')
            return redirect('register',des)
         else:  
            user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
            user.save()
            print('user created')
            user=User.objects.get(username=request.POST['username'])
            if(des =='doctor'):
                user.is_doctor=True
                user.save()
                doctor=Doctor.objects.create(user=user)
                doctor.save()

            elif(des == 'patient'):
                print('hi_pat')
                user.is_patient=True
                user.save()
            messages.info(request,'Successfully Registered')
            return redirect('login',des)
        else:
            messages.info(request,'password is not matching')
            return redirect('register',des)
           
        
        return redirect('login',des)
    else: 
        form= UserForm
        if 'submitted' in request.GET:
            submitted =True        
        return render(request,'register.html',{'form':form,'submitted':submitted})

def logout(request):
   auth.logout(request)
   return redirect('/')


        

def home(request):
    cities =City.objects.all()
    sps = Speciality.objects.all()
    return render(request,'home.html',{'cities':cities,'sps':sps})

