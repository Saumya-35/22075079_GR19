from django.shortcuts import render,redirect,get_object_or_404
from .models import Patient,Doctor,Patients_Detail,Conditions,Doctors_Detail,LabReport,Appointment,Bill,Discharge
from django.http import HttpResponseRedirect
from .forms import PatientForm,DoctorForm,LabReportForm,BookAppointmentForm,PatientDetailForm,DoctorDetailForm,ConditionForm
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q,F
from datetime import datetime
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse_lazy
from itertools import groupby
from operator import itemgetter
from django.shortcuts import render
from .models import Doctor
from django.contrib.auth.decorators import login_required


def front_page(request):
    return render(request, 'administrator/front_page.html')

def adminhome(request):
    return render(request,'administrator/admin.html')


@login_required
def viewbilllist(request):
    billdet = Bill.objects.all()
    return render(request,'administrator/viewbilllist.html',{'billdet':billdet})

@login_required
def bill(request,appoint_id):
    appoint=Appointment.objects.get(pk=appoint_id)
    patient = Patient.objects.get(pk=appoint.pid.pk)
    doctor = Doctor.objects.get(pk=appoint.did.pk)
    patient_detail = Patients_Detail.objects.get(pid=appoint.pid.pk)
    currdate = datetime.now().date()
    disdet = {
        'appoint_id':appoint,
        'pid':patient,
        'did':doctor,
        'discharge_date':currdate,
    
    }
    data = Discharge(**disdet)
    appoint.dstatus=True
    data.save()
    appoint.save()
    discharge_detail = Discharge.objects.get(Q(pid=appoint.pid.pk) & Q(appoint_id=appoint_id) & Q(did=appoint.did.pk) )
    noofdays = (discharge_detail.discharge_date-discharge_detail.reg_date).days
    return render(request,'administrator/bill.html',{'patient_detail':patient_detail,'discharge_detail':discharge_detail,'noofdays':noofdays})

@login_required
def submit_data(request,appoint_id):
    appointment = Appointment.objects.get(appoint_id=appoint_id)
    patient_detail = Patients_Detail.objects.get(pid=appointment.pid)
    discharge_detail = Discharge.objects.get(appoint_id=appoint_id)
    noofdays = (discharge_detail.discharge_date - discharge_detail.reg_date).days
    if request.method == 'POST':
        room_charges = int(request.POST.get('RoomCharges'))
        operation_charges = int(request.POST.get('OperationCharges'))
        doctor_fee = int(request.POST.get('DoctorFee'))
        labinstance = LabReport.objects.get(Q(pid=appointment.pid) & Q(did=discharge_detail.did))
        total_amount = room_charges*abs(noofdays) + operation_charges + doctor_fee + labinstance.amount
        
        
        billdet = Bill(pid=appointment.pid,
            room_charges=room_charges,
            operation_charges=operation_charges,
            doctor_fee=doctor_fee,
            total_amount=total_amount,
            appoint_id=appointment,
            amount=labinstance.amount,
            no_of_days=noofdays,
            report_no=labinstance
        )

        # Save the new instance to the database
        billdet.save()
        
        completeamount = {'billdetail':billdet}
        return render(request,'administrator/viewbilllist.html',completeamount)
    else:
        return HttpResponse("Form was not submitted.")
 
@login_required   
def viewbill(request,bill_id):
    billdetail = Bill.objects.get(pk=bill_id)
    
    patientdet = Patients_Detail.objects.get(pid=billdetail.pid)
    discharge_detail = Discharge.objects.get(appoint_id=billdetail.appoint_id)
    return render(request,'administrator/viewbill.html',{'billdetail':billdetail,'patientdet':patientdet,'discharge_detail':discharge_detail})

@login_required
def dashboard(request):
    cntpatient = Patient.objects.count()
    cntd = Doctor.objects.count()
    symptoms = Conditions.objects.all()
    
    noofpat_symp = []
    for symp in symptoms:
        cntp = Appointment.objects.filter(symptoms=symp).count()
        noofpat_symp.append({'symptom':symp,'noofpat':cntp})
    return render(request,'administrator/dashboard.html',{'cntpatient':cntpatient,'cntd':cntd,'noofpatsymp':noofpat_symp})

@login_required
def all_patients(request):
    patients = Patient.objects.all()
    return render(request,'administrator/allpatients.html',{'patients':patients,})

@login_required
def viewpatientdetail(request,patient_id):
    patient = Patient.objects.get(pk=patient_id)
    patdetail = Patients_Detail.objects.get(pid = patient_id)
    return render(request,'administrator/viewpatientdetail.html',{'patient':patient,'patdetail':patdetail})

@login_required
def viewdoctordetail(request,doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    docdetail = Doctors_Detail.objects.get(did = doctor_id)
    return render(request,'administrator/viewdoctordetail.html',{'doctor':doctor,'docdetail':docdetail})

@login_required
def all_doctors(request):
    doctors = Doctor.objects.all()
    return render(request,'administrator/alldoctors.html',{'doctors':doctors})


@login_required
def list_patient(request):
    patients = Patient.objects.all()
    
    patients_details = []
    for patient in patients:
        patient_id = patient.pk
        patient_detail = Patients_Detail.objects.get(pid=patient_id)
        patients_details.append({'patient':patient,'patient_detail':patient_detail})
    
    return render(request,'administrator/allpatients.html',{'patients_details':patients_details,})

@login_required
def list_doctor(request):
    doctors = Doctor.objects.all()
    
    doctors_details = []
    for doctor in doctors:
        doctor_id = doctor.pk
        doctor_detail = Doctors_Detail.objects.get(did=doctor_id)
        noofpatient= Patient.objects.filter(did=doctor_id).count()
        doctors_details.append({'doctor':doctor,'doctor_detail':doctor_detail,})
    
    return render(request,'administrator/alldoctors.html',{'doctors_details':doctors_details})



@login_required
def add_patient(request):
    submitted = False
    if request.method=="POST":
        formA = PatientForm(request.POST,prefix='modelA')
        formB = PatientDetailForm(request.POST,prefix='modelB')
        
        if formA.is_valid() and formB.is_valid():
            patient_data = {
                'fname':formA.cleaned_data['fname'],
                'middlename':formA.cleaned_data['middlename'],
                'lname':formA.cleaned_data['lname'],
                'birthdate':formA.cleaned_data['birthdate'],
                'gender':formA.cleaned_data['gender'],
                'status':True
            }
            
            
            
            patient = Patient(**patient_data)
            patient.save()
            patient_id = patient.pid
            patient_instance = Patient.objects.get(pid=patient_id)
            
            
            patients_detail_data = {
                'contact_no': formB.cleaned_data['contact_no'],
                'address': formB.cleaned_data['address'],
                'city': formB.cleaned_data['city'],
                'state': formB.cleaned_data['state'],
                'email': formB.cleaned_data['email'],
                'blood_group': formB.cleaned_data['blood_group'],
                'pid': patient_instance
            }
            
            patients_detail = Patients_Detail(**patients_detail_data)
          
            patients_detail.save()
            
            return HttpResponseRedirect("/administrator/add_patient?submitted=True")
    else:
        formA = PatientForm(request.POST,prefix='modelA')
        formB = PatientDetailForm(request.POST,prefix='modelB')
        if 'submitted' in request.GET:
            submitted = True
            
    return render(request,'administrator/add_patient.html',{'formA':formA,'formB':formB,'submitted':submitted})

@login_required
def add_doctor(request):
    submitted = False
    if request.method=="POST":
        forma = DoctorForm(request.POST,prefix='modela')
        formb = DoctorDetailForm(request.POST,prefix='modelb')
        if forma.is_valid() and formb.is_valid():
            doctor_data = {
                'dname': forma.cleaned_data['dname'],
                'specialisation' : forma.cleaned_data['specialisation'],
            }
            
            
            
            doctor = Doctor(**doctor_data)
            doctor.save()
            doctor_id = doctor.did
            doctor_instance = Doctor.objects.get(did=doctor_id)
            
            doctors_detail_data = {
                'contact_no': formb.cleaned_data['contact_no'],
                'address': formb.cleaned_data['address'],
                'email': formb.cleaned_data['email'],
                'did': doctor_instance
            }
            
            doctors_detail = Doctors_Detail(**doctors_detail_data)
          
            doctors_detail.save()
            
            return HttpResponseRedirect("/administrator/add_doctor?submitted=True")
    else:
        forma = DoctorForm(request.POST,prefix='modela')
        formb = DoctorDetailForm(request.POST,prefix='modelb')
        if 'submitted' in request.GET:
            submitted = True
            
    return render(request,'administrator/add_doctor.html',{'forma':forma,'submitted':submitted,'formb':formb})

@login_required
def search_patient(request):
    found=False
    if request.method == "POST":
        searched = request.POST['searched']
        patients = Patient.objects.filter(Q(fname__icontains=searched) | Q(middlename__icontains=searched) | Q(lname__icontains=searched))
       
        
        return render(request,'administrator/searchpatient.html',{'searched':searched,'patients':patients,'found':found})
        
    else:
        return render(request,'administrator/searchpatient.html',{})
    
@login_required  
def search_doctor(request):
    
    if request.method == "POST":
        searched = request.POST['searched']
        doctors = Doctor.objects.filter(dname__icontains=searched)
       
        return render(request,'administrator/searchdoctor.html',{'searched':searched,'doctors':doctors})
        
    else:
        return render(request,'administrator/searchdoctor.html',{})
    

    
@login_required
def addlabreport(request,appoint_id):
    submitted = False
    appoint = Appointment.objects.get(pk=appoint_id)
    patient_name = f"{appoint.pid.fname} {appoint.pid.lname}"
    if request.method=="POST":
        patient = Patient.objects.get(pk=appoint.pid.pk)
        doctor = Doctor.objects.get(pk=appoint.did.pk)
        form = LabReportForm(request.POST, initial={'patient_name': patient_name})
        if form.is_valid():
            
            
            lab_data = {
                'pid':patient,
                'sample_date' : form.cleaned_data['sample_date'],
                'did':doctor,
                'phlev' : form.cleaned_data['phlev'],
                'chlolev' : form.cleaned_data['chlolev'],
                'sucrlev' : form.cleaned_data['sucrlev'],
                'wbcratio' : form.cleaned_data['wbcratio'],
                'rbcratio' : form.cleaned_data['rbcratio'],
                'reports' : form.cleaned_data['reports'],
                'appoint_id': appoint,
                'amount':  form.cleaned_data['amount']
            }
            
            lab = LabReport(**lab_data)
            appoint.lstatus=True
            lab.save()
            appoint.save()
            return HttpResponseRedirect("/administrator/labreportlist?submitted=True")
    else:
        form = LabReportForm(initial={'patient_name': patient_name})
        if 'submitted' in request.GET:
            submitted = True
            
    return render(request,'administrator/labreport.html',{'form':form,'submitted':submitted})

@login_required
def labreportlist(request):
    appoint = Appointment.objects.all()
    lab_detail = []
    for app in appoint:
        try:
            labrep = LabReport.objects.get(appoint_id=app.pk)
            lab_detail.append({'app': app, 'labrep': labrep})
        except LabReport.DoesNotExist:
           lab_detail.append({'app': app, 'labrep': ''})
             
        
    return render(request,'administrator/labreportlist.html',{'lab_detail':lab_detail})  
       
@login_required       
def viewreport(request,report_no):
    lab_report = LabReport.objects.get(report_no=report_no)
    return render(request,'administrator/viewreport.html',{'lab_report':lab_report})


@login_required
def bookappointment(request):
    submitted = False
    if request.method=="POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            
          
            patient_id = form.cleaned_data['pid']
            patient = Patient.objects.get(pk=patient_id)
            symptoms = form.cleaned_data['symptoms']
            doctor_id = form.cleaned_data['did']
            doctor = Doctor.objects.get(pk=doctor_id)
            appoint_data = {
                'pid': patient,
                'date': form.cleaned_data['date'],
                'time': form.cleaned_data['time'],
                'did': doctor,
                'symptoms':symptoms
            }
            
            appointment = Appointment(**appoint_data)
            appointment.save()
            
            return HttpResponseRedirect("/administrator/bookappointment?submitted=True")
    else:
        form = BookAppointmentForm()
        
        if 'submitted' in request.GET:
            submitted = True
            
    return render(request,'administrator/bookappointment.html',{'form':form,'submitted':submitted})


@login_required
def display_doctors_by_specialization(request):
    doctors = Doctor.objects.all().order_by('specialisation')  # Retrieve all doctors and order them by specialization

    grouped_doctors = {}
    for specialization, group in groupby(doctors, key=lambda x: x.specialisation):
        grouped_doctors[specialization] = list(group)

    return render(request, 'administrator/your_template.html', {'grouped_doctors': grouped_doctors})


@login_required
def display_patients(request):
    patients = Patient.objects.all() # Retrieve all doctors and order them by specialization

    return render(request, 'administrator/my_template.html', {'patients': patients})


@login_required
def displayappointment(request):
    appointments = Appointment.objects.all()
    patient = Patient.objects.filter(status=False)
    patients_details = []
    previousstatusc = Appointment.objects.filter(lstatus=True).count()
    currentstatusc = Appointment.objects.filter(lstatus=False).count()
    
    message= None
    if not patient:
        message = ""
    else:
        
        for pat in patient:
            patient_id = pat.pk
            patient_detail = Patients_Detail.objects.get(pid=patient_id)
            patients_details.append({'pat':pat,'patient_detail':patient_detail})
    return render(request,'administrator/displayappointment.html',{'appointments':appointments,'patient_detail':patients_details,'message':message,'previousstatusc':previousstatusc,'currentstatusc':currentstatusc})

@login_required  
def condition(request):
    submitted = False
    if request.method=="POST":
        form = ConditionForm(request.POST)
        if form.is_valid():
            
            
            cond_data = {
                'symptoms': form.cleaned_data['symptoms'],
                'specialisation': form.cleaned_data['specialisation'],
            }
            
            cond= Conditions(**cond_data)
            cond.save()
            
            return HttpResponseRedirect("/administrator/condition?submitted=True")
    else:
        form = ConditionForm()
        if 'submitted' in request.GET:
            submitted = True
            
    return render(request,'administrator/condition.html',{'form':form,'submitted':submitted})
    
@login_required
def updatepatient(request,patient_id):
    patient = Patient.objects.get(pk=patient_id)
    patient_detail = Patients_Detail.objects.get(pid=patient_id)
    forma = PatientForm(request.POST or None, instance=patient)
    formb = PatientDetailForm(request.POST or None, instance=patient_detail)
    if forma.is_valid() and formb.is_valid():
        forma.save()
        formb.save()
        
        return redirect('list-patient')
    
    return render(request,'administrator/updatepatient.html',{'patient':patient,'forma':forma,'formb':formb})

@login_required
def updatedoctor(request,doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    doctor_detail = Doctors_Detail.objects.get(did=doctor_id)
    forma = DoctorForm(request.POST or None, instance=doctor)
    formb = DoctorDetailForm(request.POST or None, instance=doctor_detail)
    if forma.is_valid() and formb.is_valid():
        forma.save()
        formb.save()
        
        return redirect('all-doctors')
    
    return render(request,'administrator/updatedoctor.html',{'doctor':doctor,'forma':forma,'formb':formb})

@login_required   
def confirmdeletepatient(request,patient_id):
    try:
        patient = Patient.objects.get(pk=patient_id)
        patient_details = Patients_Detail.objects.filter(pid=patient)
        patient_details.delete()
        patient.delete()
        return redirect('list-patient')
    except Patient.DoesNotExist:
        return render(request, 'patientnotfound.html')
 
@login_required    
def confirmdeletedoctor(request,doctor_id):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        doctor_details = Doctors_Detail.objects.filter(did=doctor)
        doctor_details.delete()
        doctor.delete()
        return redirect('list-doctor')
    except Doctor.DoesNotExist:
        return render(request, 'doctornotfound.html')

@login_required    
def dischargelist(request):
    appoint = Appointment.objects.all()
    cnt = Appointment.objects.filter(Q(lstatus=True) & Q(dstatus=False)).count()
    
    whole_details = []

    for appointment in appoint:
            # Retrieve the associated doctor for each appointment
            patient = Patient.objects.get(pid=appointment.pid.pk)
            doctor = Doctor.objects.get(did=appointment.did.pk)
            pdet = Patients_Detail.objects.get(pid=appointment.pid.pk)
            whole_details.append({'doctor':doctor,'patient':patient,'appointment':appointment,'pdet':pdet})
    return render(request,'administrator/dischargelist.html',{'whole_details':whole_details,'cnt':cnt})

@login_required
def viewappointment(request,appoint_id):
    appoint_detail = Appointment.objects.get(appoint_id=appoint_id)
    return render(request,'administrator/viewappointment.html',{'appoint_detail':appoint_detail})

@login_required
def allcount(request):
    cntp = Patient.objects.count()
    cntd = Doctor.objects.count()
    return render(request,'administrator/dashboard.html',{'cntp':cntp,'cntd':cntd})

