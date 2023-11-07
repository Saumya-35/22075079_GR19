from django import forms 
from django.forms import ModelForm
from .models import (Patient,Patients_Detail,Doctor,Appointment,Conditions,Doctors_Detail)

#creste a patient regiter form
bgroup = [
    ('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-')
]
symptom = [
    ("Heart and Cardiovascular","Heart and Cardiovascular"),
    ("skin, hair, nails, and mucous membranes","skin, hair, nails, and mucous membranes"),
    ("life-threatening medical conditions","life-threatening medical conditions"),("allergies and immunological disorder","allergies and immunological disorder"),("anesthesia","anesthesia "),("colon,rectum,and anus","colon,rectum,and anus")
    
]

gend = [
    ('F','Female'),('M','Male'),('O','Other')
]
    
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['fname','middlename','lname','birthdate','gender',]
        
        fname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        middlename = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        lname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        birthdate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
        gender = forms.ChoiceField(choices=gend, widget=forms.Select(attrs={'class': 'form-control'}))
        
        
class PatientDetailForm(forms.ModelForm):
    class Meta:
        model = Patients_Detail
        fields=['contact_no','address','city','state','email','blood_group']
        
        
        contact_no = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
        address= forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
        city= forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
        state= forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
        email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control'}))
        blood_group = forms.CharField(widget = forms.Select(attrs={'class':'form-control'},choices=bgroup))
    
    
# departments=[('Cardiologist','Cardiologist'),
# ('Dermatologists','Dermatologists'),
# ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
# ('Allergists/Immunologists','Allergists/Immunologists'),
# ('Anesthesiologists','Anesthesiologists'),
# ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
# ]
    
class DoctorForm(forms.ModelForm):
     class Meta:
        model = Doctor
        fields=['dname','specialisation']
       
        dname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
        specialisation = forms.ModelChoiceField(
        queryset= Conditions.objects.all(),  
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
        

class DoctorDetailForm(forms.ModelForm):
    class Meta:
        model = Doctors_Detail
        fields=['contact_no','address','email']
        
        
        contact_no = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
        address= forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}),required=False)
        email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control'}),required=False)
    

class LabReportForm(forms.Form):
    pid = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}))
    sample_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}),required=False)
    did = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phlev = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)
    chlolev = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)
    sucrlev = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)
    wbcratio = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)
    rbcratio = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)
    reports = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)
    appoint_id = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),required=False
    )
    
   
class BookAppointmentForm(forms.Form):
    pid = forms.ChoiceField(widget= forms.Select(attrs={'class':'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control'}))
    symptoms = forms.ModelChoiceField(
        queryset=Conditions.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a symptom",
    )
    did = forms.ChoiceField(
         widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    
    def __init__(self, *args, **kwargs):
        super(BookAppointmentForm, self).__init__(*args, **kwargs)
        patients = Patient.objects.all().values_list('pid', 'pid')
        self.fields['pid'].choices = patients
        
        doctors = Doctor.objects.all().values_list('did', 'did')
        self.fields['did'].choices = doctors

     
class ConditionForm(forms.ModelForm):
        
    class Meta:
        model = Conditions
        fields='__all__'
        
    symptoms = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control'}))
    specialisation = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control'}))
        
        

    
  
   

        