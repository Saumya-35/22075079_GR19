from django import forms
from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q


    

# Create your models here.
departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]


class Doctor(models.Model):
    did = models.BigAutoField(primary_key=True)
    dname = models.CharField('Doctor Name', max_length=100, default=None)
    specialisation = models.CharField('Specialization', max_length=50, choices=departments, default=None,null=False)

    class Meta:
            db_table = 'Doctor'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.dname


 

class Doctors_Detail(models.Model):
    did = models.OneToOneField(Doctor,on_delete=models.CASCADE,primary_key=True)
    email = models.EmailField(max_length=30,null=True,blank=True,unique=True)
    address = models.TextField(max_length=50,null=True,blank=True)
    contact_no = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'Doctors_Detail'
    
    def __str__(self):
        return f"{self.did.dname}"

    
GENDER_CHOICES = [
   ("F","Female"),
    ("M","Male"),
    ("O","Other")]    


    
class Patient(models.Model):
    pid = models.BigAutoField(primary_key=True)
    did = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True)
    fname = models.CharField('First Name',max_length=30)
    middlename = models.CharField('Middle Name',max_length=30,null=True,blank=True)
    lname = models.CharField('Last Name',max_length=30,null=True,blank=True)
    birthdate = models.DateField('Date of Birth')
    gender = models.CharField('Gender',max_length=1,
                        choices=GENDER_CHOICES)
    status=models.BooleanField(default=False)
    apstatus = models.BooleanField(default=False)
    class Meta:
        db_table = 'Patient'
    
    def __str__(self):
        return self.fname + ' ' + self.lname
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.birthdate.year - ((today.month, today.day) <
                (self.birthdate.month, self.birthdate.day))
        
        return age
    
symptom = [
    ("Heart and Cardiovascular","Heart and Cardiovascular"),
    ("skin, hair, nails, and mucous membranes","skin, hair, nails, and mucous membranes"),
    ("life-threatening medical conditions","life-threatening medical conditions"),("allergies and immunological disorder","allergies and immunological disorder"),("anesthesia","anesthesia "),("colon,rectum,and anus","colon,rectum,and anus")
    
]

class Conditions(models.Model):
    symptoms = models.CharField(primary_key=True,max_length=50,default=None)
    specialisation = models.CharField('Specialization', max_length=50, default=None)
    
    class Meta:
        db_table = 'Conditions'
        
    def __str__(self):
        return self.symptoms
    
    
bgroup = [
    ('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-')
]
class Patients_Detail(models.Model):
    pid = models.ForeignKey(Patient,on_delete=models.CASCADE,default=None)
    contact_no = models.CharField(max_length=10,primary_key=True,default=None)
    address = models.TextField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=20,blank=True,null=True)
    state = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(max_length=30,blank=True,null=True)
    blood_group = models.CharField(max_length=3,choices=bgroup, default='B+')
    
    class Meta:
        db_table = 'Patients_Detail'
   
    
    def __str__(self):
        return f"{self.pid.fname} {self.pid.lname}"
    
class Appointment(models.Model):
    appoint_id = models.BigAutoField(primary_key=True)
    did = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True)
    pid = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField('Date of appointment')
    time = models.TimeField('Time of appointment')
    symptoms = models.CharField(choices=symptom,max_length=50,blank=True,null=True)
    dstatus=models.BooleanField(default=False)#discharge status
    lstatus=models.BooleanField(default=False)#labreport status
 
    
    class Meta:
        db_table = 'Appointment'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return f"{self.pid.fname} {self.pid.lname}"   


class LabReport(models.Model):
    report_no = models.BigAutoField(primary_key=True)
    pid =models.ForeignKey(Patient,on_delete=models.CASCADE,default=None)
    sample_date = models.DateField('Sample Date')
    did = models.ForeignKey(Doctor,on_delete=models.CASCADE,default=None)
    amount = models.IntegerField('Amount',default=0)
    appoint_id = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    phlev = models.DecimalField('Ph level',max_digits=5,decimal_places=2,default=0,null=True)
    chlolev = models.DecimalField('Cholesterol level',max_digits=5,decimal_places=2,default=0,null=True)
    sucrlev = models.DecimalField('Sucrose level',max_digits=5,decimal_places=2,default=0,null=True)
    wbcratio = models.IntegerField('WBC ratio',default=0)
    rbcratio = models.IntegerField('RBC ratio',default=0)
    reports = models.CharField('Reports',max_length=50,null=True,blank=True)
    status=models.BooleanField(default=False)
    patient_name = models.CharField('Patient Name', max_length=100, editable=False, blank=True)
    
    class Meta:
        db_table = 'LabReport'
    
    def __str__(self):
        return f"{self.pid.fname} {self.pid.lname}"
    
    
 
    
    

class Bill(models.Model):
    bill_no = models.BigAutoField(primary_key=True,default=None,blank=True)
    pid = models.ForeignKey(Patient,on_delete=models.CASCADE)
    room_charges = models.IntegerField('Room Charges',default=0)
    operation_charges = models.IntegerField('Operation Charges',default=0)
    doctor_fee = models.IntegerField('Doctor Fee',default=0)
    report_no = models.ForeignKey(LabReport,on_delete=models.CASCADE)
    no_of_days = models.IntegerField('No Of Days Stayed',default=0,blank=True)
    amount = models.IntegerField('Amount',default=0,blank=True)
    total_amount = models.IntegerField('Total Amount',default=0,blank=True)
    appoint_id = models.ForeignKey(Appointment,on_delete=models.CASCADE,blank=True,null=True)
    
    class Meta:
        db_table = 'Bill'
        
    def save(self,*args,**kwargs):
        el = Discharge.objects.get(appoint_id=self.appoint_id)
        if el.reg_date and el.discharge_date :
            self.no_of_days = (el.discharge_date - el.reg_date).days 
            
        else:
            self.no_of_days = 0
            
        self.amount = self.report_no.amount
            
        self.total_amount = self.room_charges*(self.no_of_days) + self.operation_charges + self.amount + self.doctor_fee
        super(Bill,self).save(*args,**kwargs)
    
    
    def __str__(self):
        return f"{self.pid.fname} {self.pid.lname}" 

    
    
class Discharge(models.Model):
    appoint_id = models.OneToOneField(Appointment,on_delete=models.CASCADE,primary_key=True)
    pid = models.ForeignKey(Patient,on_delete=models.CASCADE)
    did = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    reg_date = models.DateField('Registration Date',blank=True)
    discharge_date = models.DateField('Discharge Date',auto_now=True)
  
    
    class Meta:
        db_table = 'Discharge'
    def save(self,*args,**kwargs):
        appointment = Appointment.objects.get(appoint_id=self.appoint_id_id)
        self.reg_date = appointment.date
        super(Discharge,self).save(*args,**kwargs)
        
    def __str__(self):
         return f"{self.pid.fname} {self.pid.lname}"
    


    
    
    
    
    
    

