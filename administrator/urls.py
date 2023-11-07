from django.urls import path
from . import views

urlpatterns = [
    path("",views.adminhome,name='admin-home'),
    path('addpatient/',views.add_patient,name='add-patient'),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("allpatients/",views.all_patients,name='all-patients'),
    path("viewpatientdetail/<patient_id>",views.viewpatientdetail,name='viewpatientdetail'),
    path("viewdoctordetail/<doctor_id>",views.viewdoctordetail,name='viewdoctordetail'),
    path("alldoctors/",views.all_doctors,name='all-doctors'),
    path("add_patient/",views.add_patient,name="add-patient"),
    path("add_doctor/",views.add_doctor,name='add-doctor'),
    path("listpatient/",views.list_patient,name='list-patient'),
    path("listdoctor/",views.list_doctor,name='list-doctor'),
    path("search_patient/",views.search_patient,name='search-patient'),
    path("search_doctor/",views.search_doctor,name='search-doctor'),
    path("addlabreport/<appoint_id>",views.addlabreport,name='add-lab-report'),
    path("labreportlist/",views.labreportlist,name='lab-report-list'),
    path("viewreport/<report_no>",views.viewreport,name='view-report'),
    path("bookappointment/",views.bookappointment,name='book-appointment'),
    path("displayappointment/",views.displayappointment,name='display-appointment'),
    path("viewappointment/<appoint_id>",views.viewappointment,name='view-appointment'),
    path("update_patient/<patient_id>",views.updatepatient,name='update-patient'),
    path("update_doctor/<doctor_id>",views.updatedoctor,name='update-doctor'),
    path("condition/",views.condition,name="condition"),
    path("p_delete/<patient_id>",views.confirmdeletepatient,name='patient-confirm-delete'),
    path("d_delete/<doctor_id>",views.confirmdeletedoctor,name='doctor-confirm-delete'),
    path("submit_data/<appoint_id>",views.submit_data,name='submit_data'),
    path("dischargelist/",views.dischargelist,name='dischargelist'),
    path('viewbilllist/', views.viewbilllist, name='view-bill-list'),
    path("bill/<appoint_id>",views.bill,name='bill'),
    path("viewbill/<bill_id>",views.viewbill,name='viewbill'),
    path('groupdoctor/',views.display_doctors_by_specialization,name="group-doctor"),
    path('front_page/',views.front_page,name="front_page"),
    path('patient/',views.display_patients, name='patient'),
]