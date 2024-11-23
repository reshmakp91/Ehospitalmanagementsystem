from django.shortcuts import render,redirect,get_object_or_404
from adminapp.models import *
from adminapp.forms import *
from django.contrib import messages
from doctorapp.models import *
from doctorapp.forms import *
from django.db.models import Prefetch
from functools import wraps
from accountsapp.views import *
from django.http import HttpResponse

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_id = request.session.get('admin_id')
        print(f"Admin ID in decorator: {admin_id}")  # Debugging
        print(f"Session Data: {request.session.items()}")  # Debugging

        if not admin_id:
            print("Redirecting to login due to missing admin_id")
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
def test_view(request):
    return HttpResponse("Admin access verified")


@admin_required
def adminpanel(request):
    patients = PatientProfile.objects.all()
    facilities = Facility.objects.all()
    doctors = DoctorProfile.objects.all()
    appointments = Appointment.objects.all()
    total_facilities = facilities.count()
    total_patients = patients.count()
    total_doctors = doctors.count()
    total_facilities = facilities.count()
    scheduled_appointments = Appointment.objects.filter(status='Scheduled')
    return render(request,'adminapp/dashboard.html',{
        'total_facilities': total_facilities,
        'total_doctors':total_doctors,
        'total_patients':total_patients,
        'appointments' : scheduled_appointments
    })

@admin_required
def patientcreate(request):
    if request.method == 'POST':
        patientform = PatientProfileForm(request.POST, request.FILES)
        if patientform.is_valid():
            patientform.save()
            messages.success(request,'Form submitted successfully')
    else:
        patientform = PatientProfileForm()
    return render(request, 'adminapp/PatientCreate.html', {'patientform': patientform})

@admin_required
def doctorcreate(request):
    if request.method == 'POST':
        doctorform = DoctorProfileForm(request.POST,request.FILES)
        if doctorform.is_valid():
            doctorform.save()
            messages.success(request, 'Form submitted successfully')
    else:
        doctorform = DoctorProfileForm()
    specializations = DEPARTMENT_CHOICES
    facilities = Facility.objects.all()
    return render(request,'adminapp/DoctorCreate.html',{'doctorform' : doctorform, 'specializations': specializations,'facilities':facilities})

@admin_required
def facilitycreate(request):
    if request.method == 'POST':
        facilityform = Facilityform(request.POST,request.FILES)
        if facilityform.is_valid():
            facilityform.save()
            messages.success(request, 'Form submitted successfully')
    else:
        facilityform = Facilityform()
    return render(request,'adminapp/FacilityCreate.html',{'facilityform' : facilityform})


@admin_required
def facilities(request):
    facilities = Facility.objects.all()
    return render(request, 'adminapp/facilities.html', {'facilities': facilities})

@admin_required
def doctors(request):
    doctors = DoctorProfile.objects.all()
    departments = DEPARTMENT_CHOICES
    facilities = Facility.objects.all()
    return render(request,'adminapp/doctors.html', {'doctors':doctors, 'departments' : departments,'facilities': facilities})

@admin_required
def patients(request):
    patients = PatientProfile.objects.all()
    return render(request,'adminapp/patients.html',{'patients':patients})

@admin_required
def appointments(request):
    appointments = Appointment.objects.prefetch_related(Prefetch('payment_set', queryset=Payment.objects.all()))
    appointment_data = []
    for appointment in appointments:
        payments = appointment.payment_set.all()
        appointment_data.append({'appointment': appointment,'payments': payments,})
    return render(request, 'adminapp/appointments.html', {'appointment_data': appointment_data})

@admin_required
def facility_detail(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    doctors = DoctorProfile.objects.filter(facility=facility)
    departments = DEPARTMENT_CHOICES
    resources = RESOURCE_CHOICES
    selected_departments = facility.departments
    selected_resources = facility.resources
    context = {
        'facility': facility,
        'doctors': doctors,
        'departments' : departments,
        'resources' : resources ,
        'selected_departments': selected_departments,
        'selected_resources': selected_resources
    }
    return render(request, 'adminapp/facility_detail.html', context )

@admin_required
def appointment_detail(request, id):
    appointment = get_object_or_404(Appointment,id=id)
    doctors = DoctorProfile.objects.all()
    return render(request,'adminapp/appointmentdetails.html',{'appointment':appointment,'doctors': doctors})

@admin_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    medical_history = MedicalHistory.objects.filter(patient=patient)
    prescription = Prescription.objects.filter(patient=patient)
    return render(request, 'adminapp/patientdetail.html', {
        'patient': patient,
        'appointments': appointments,
        'medical_history' : medical_history,
        'prescription' : prescription
    })

@admin_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        doctor_instance = get_object_or_404(DoctorProfile, id=doctor_id)
        appointment.appointment_date = request.POST['appointment_date']
        appointment.doctor = doctor_instance
        appointment.reason = request.POST['reason']
        appointment.status = request.POST['status']
        appointment.save()
        messages.success(request, 'Appointment details updated successfully')
        return redirect('appointment_detail', id=appointment.id)
    doctors = DoctorProfile.objects.all()
    return render(request, 'adminapp/appointmentdetails.html', {'appointment': appointment,'doctors': doctors})

@admin_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient details updated successfully.")
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientProfileForm(instance=patient)
    return render(request, 'adminapp/edit_patient.html', {'form': form, 'patient': patient})


@admin_required
def edit_doctor(request, id):
    doctor = get_object_or_404(DoctorProfile, id=id)
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.specialization = request.POST.get('specialization')
        doctor.facility_id = request.POST.get('facility')
        doctor.contact = request.POST.get('contact')
        doctor.email = request.POST.get('email')
        if 'image' in request.FILES:
            doctor.image = request.FILES['image']
        doctor.save()
        messages.success(request, 'Doctor details updated successfully')
        return redirect('doctors')
    return render(request, 'adminapp/doctors.html')

@admin_required
def edit_facility(request,id):
    facility = get_object_or_404(Facility,id=id)
    if(request.method == 'POST'):
        form = Facilityform(request.POST, request.FILES,instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, 'Details updated successfully')
            return redirect('facility_detail', facility_id=id)
    else:
        form = Facilityform(instance=facility)
    return render(request,'adminapp/facility_detail.html',{'form' : form})


@admin_required
def MedicalHistoryPatientList(request):
    patients = PatientProfile.objects.all()
    return render(request, 'adminapp/medical_patients.html', {'patients': patients})


@admin_required
def MedicalHistory_List(request,patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    doctor_ids = appointments.values_list('doctor', flat=True)
    doctors = DoctorProfile.objects.filter(id__in=doctor_ids)
    return render(request, 'adminapp/MedicalHistoryList.html', {'doctors': doctors, 'patient':patient})

@admin_required
def View_Medical_History(request, doctor_id, patient_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    patient = get_object_or_404(PatientProfile, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient, doctor=doctor)
    medical_histories = MedicalHistory.objects.filter(patient=patient, doctor=doctor)
    appointment_histories = []
    for appointment in appointments:
        history = medical_histories.filter(appointment=appointment).first()
        prescriptions = Prescription.objects.filter(medical=history) if history else []
        appointment_histories.append({'appointment': appointment, 'history': history,'prescriptions': prescriptions,})
    return render(request, 'adminapp/medicalhistoryview.html', {'doctor': doctor,'appointment_histories': appointment_histories,})

@admin_required
def payments(request):
    payments = Payment.objects.all()
    return render(request,'adminapp/payments.html',{'payments':payments})
