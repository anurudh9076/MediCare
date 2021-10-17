from django.shortcuts import render,redirect
from .models import Doctor,City,Speciality,Appointment,Slots,Patient
from .filters import DoctorFilter
from .forms import UserForm,User,DoctorForm
from django.contrib.auth.models import auth
from django.contrib import messages
import datetime

import smtplib
import django
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.

def view_profile(request):
    if request.user is None:
        return redirect('home')
    if request.user.is_doctor:
        doctor=Doctor.objects.get(user=request.user)
        slots=Slots.objects.filter(doctor=doctor)
        return render(request,'view_profile.html',{'doctor':doctor,'slots':slots})


def done_appointment(request,app_id):
    user=request.user
    if user is None:
        return redirect('/')
    if user.is_patient:
        return redirect('/')
    
    appointment=Appointment.objects.get(id=app_id)
    appointment.status='Completed'
    appointment.editable=False
    appointment.save()
    return redirect('view-appointments')

def cancel_appointment(request,app_id):
    user=request.user
    if user is None:
        return redirect('/')
    appointment=Appointment.objects.get(id=app_id)
    appointment.status='Cancelled'
    if user.is_doctor:
        appointment.cancelled_by_doctor=True
    else:
        appointment.cancelled_by_patient=True
    appointment.editable=False
    appointment.save()
    return redirect('view-appointments')
def view_appointments(request):
    user=request.user
    if user is None:
        redirect('home')
    if user.is_doctor:
        doctor=Doctor.objects.get(user=request.user.id)
        appointments=Appointment.objects.filter(doctor=doctor).order_by('date')
        editable=[]
        for ap in appointments:
            if ap.status!="Pending":
                ap.editable=False
            if ap.date < datetime.date.today():
                if ap.status=="Pending":
                    ap.status="Uncompleted"
                ap.editable=False
            if ap.date == datetime.date.today():
                if  ap.slot.time.strftime("%H:%M:%S") < datetime.datetime.now().strftime("%H:%M:%S"):
                    ap.status="Uncompleted"
                    ap.editable=False

            ap.save()             
        return render(request,'view_appointments.html',{'appointments':appointments})
    if user.is_patient:
        appointments=Appointment.objects.filter(patient=user.id).order_by('date')
        editable=[]
        for ap in appointments:
            if ap.status!="Pending":
                ap.editable=False
            if ap.date < datetime.date.today():
                if ap.status=="Pending":
                    ap.status="Uncompleted"
                ap.editable=False
            if ap.date == datetime.date.today():
                if  ap.slot.time.strftime("%H:%M:%S") < datetime.datetime.now().strftime("%H:%M:%S"):
                    ap.status="Uncompleted"
                    ap.editable=False

            ap.save()   
        return render(request,'view_appointments.html',{'appointments':appointments})

def appoint(request):
    #doctor=Doctor.objects.get(id=doctor_id)
    if request.method=='POST':
        slot=Slots.objects.get(id=int(request.POST['slot']))
        date=request.POST['date']
        doctor =Doctor.objects.get(id=int(request.POST['doctor_id']))
        appointment=Appointment.objects.create(slot=slot,date=date,patient=request.user,doctor=doctor,status='Pending')
        appointment.save()
        print("appointment created")
        #sending the emails to doctor and client
        sender_address = 'medicare9076@gmail.com'
        sender_pass = 'Medicare#54321'
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
       
        receiver_address=request.user.email
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Appointment Of MediCare'   #The subject line
        #The body and the attachments for the mail
        mail_content='Hello '+request.user.first_name+'\n'+'you have booked an apppointment on MediCare.'
        mail_content+='See below details\n'+'Doctor: '+doctor.user.first_name+' '+doctor.user.last_name
        mail_content+='\nDate: '+date + '\nTime: '+slot.time.strftime('%H:%M %p')+'.'
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        #to doctor
        receiver_address=doctor.user.email
        message1 = MIMEMultipart()
        message1['From'] = sender_address 
        message1['To'] = receiver_address
        message1['Subject'] = 'Appointment Of MediCare'
        
        
       
        mail_content=""
        mail_content='Hello '+doctor.user.first_name+'\n'+'you have an apppointment on MediCare.'
        mail_content+='See below details\n'+'Patient: '+request.user.first_name+' '+request.user.last_name
        mail_content+='\nDate: '+date + '\nTime: '+slot.time.strftime('%H:%M %p')+'.'
        message1.attach(MIMEText(mail_content, 'plain'))
        text = message1.as_string()
        session.sendmail(sender_address, receiver_address, text)

        session.quit()
        print('Mail Sent')

        return render (request,'view_appointments.html')

    return redirect('/make-appointment')

def make_appointment(request,doctor_id):
    dated=False
    if(request.method=='POST'):
        dated=True
        date=request.POST['date']
        doctor=Doctor.objects.get(id=doctor_id)
        slots=Slots.objects.filter(doctor=doctor)
        pre_appointment=Appointment.objects.filter(doctor=doctor.id,date=date)
        pre_slosts = []
        slots=list(slots)
        for ap in pre_appointment:
            if ap.status!='Cancelled':
                slots.remove(ap.slot)

        return render(request,'make_appointment.html',{'slots':slots,'dated':dated,'date':date,'doctor':doctor})
    else:
        return render(request,'make_appointment.html',{'dated':dated})



def doctor_profile(request):
    user=request.user
    if not user.is_doctor:
        redirect('home')
    doctor=Doctor.objects.get(user=user.id)
    form = DoctorForm(request.POST or None,request.FILES or None,instance=doctor)
    form1=  UserForm(instance=user)
    if form.is_valid():
        form.save()
        messages.info(request,'Details Updated Successfully')
        return redirect('doctor-profile')

    return render (request,'doctor_profile.html',{'form':form,'user':user,'form1':form1})


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


        
def search_doctors(request):
    
    if request.method == "POST":
        if(request.POST['city'] == "select a city" and request.POST['speciality']=='select a speciality'):
            return render (request,'search_doctors.html',{'searched':False})
        elif(request.POST['speciality']=='select a speciality'):
            city=City.objects.get(name=request.POST['city'])
            doctors = Doctor.objects.filter(city=city.id)
        elif(request.POST['city'] == 'select a city'):
            speciality= Speciality.objects.get(name=request.POST['speciality'])
            doctors = Doctor.objects.filter(city=speciality.id)
        else:
            city=City.objects.get(name=request.POST['city'])
            speciality= Speciality.objects.get(name=request.POST['speciality'])
            doctors = Doctor.objects.filter(city=city.id,speciality=speciality.id)

        return render (request,'search_doctors.html',{'doctors':doctors,'searched':True})
    else:
        return render (request,'search_doctors.html',{})

def home(request):
    cities =City.objects.all()
    sps = Speciality.objects.all()
    return render(request,'home.html',{'cities':cities,'sps':sps})

