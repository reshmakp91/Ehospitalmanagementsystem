from django.shortcuts import render,redirect,get_object_or_404
from adminapp.models import *
from adminapp.forms import *
from doctorapp.models import *
from django.contrib import messages
from doctorapp.forms import *
from functools import wraps
from pharmacyapp.models import *

def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('doctor_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@doctor_required
def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(DoctorProfile,id=doctor_id)
    patients = PatientProfile.objects.all()
    facilities = Facility.objects.all()
    doctors = DoctorProfile.objects.all()
    appointments = Appointment.objects.filter(doctor=doctor)
    total_facilities = facilities.count()
    total_patients = patients.count()
    total_doctors = doctors.count()
    total_facilities = facilities.count()
    scheduled_appointments = Appointment.objects.filter(status='Scheduled', doctor=doctor)
    return render(request,'doctorapp/dashboard.html',{
        'total_facilities': total_facilities,
        'total_doctors':total_doctors,
        'total_patients':total_patients,
        'appointments' : appointments,
        'doctor': doctor,
        'scheduled_appointments' : scheduled_appointments
    })

@doctor_required
def appointments(request):
    doctor_id = request.session.get('doctor_id')
    doctor = DoctorProfile.objects.get(id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request,'doctorapp/appointments.html',{'appointments' : appointments})

@doctor_required
def appointment_detail(request, id):
    appointment = get_object_or_404(Appointment,id=id)
    return render(request,'doctorapp/appointmentdetails.html',{'appointment':appointment})

@doctor_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        appointment.status = request.POST['status']
        appointment.save()
        messages.success(request, 'Appointment details updated successfully')
        return redirect('doc_appointment_detail', id=appointment.id)
    return render(request, 'doctorapp/appointmentdetails.html', {'appointment': appointment})

@doctor_required
def patients(request):
    doctor_id = request.session.get('doctor_id')
    doctor = DoctorProfile.objects.get(id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)
    patient_ids = appointments.values_list('patient', flat=True)
    patients = PatientProfile.objects.filter(id__in=patient_ids)
    return render(request,'doctorapp/my_patients.html',{'patients': patients})

@doctor_required
def patient_detail(request, patient_id):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(DoctorProfile,id=doctor_id)
    patient = get_object_or_404(PatientProfile, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient,doctor=doctor)
    medical_history = MedicalHistory.objects.filter(patient=patient)
    prescription = Prescription.objects.filter(patient=patient)
    return render(request, 'doctorapp/patientdetail.html', {
        'patient': patient,
        'appointments': appointments,
        'medical_history' : medical_history,
        'prescription' : prescription
    })

@doctor_required
def update_MedicalDetails(request, appointment_id):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    appointment = get_object_or_404(Appointment, id=appointment_id)
    medical_history, created = MedicalHistory.objects.get_or_create(
        doctor=doctor,
        appointment=appointment,
        patient=appointment.patient,
        defaults={
            'date': appointment.appointment_date,
            'diagnosis': 'Nil',
            'treatment_description': 'Nil',
            'notes': 'Nil',
        }
    )
    if request.method == 'POST':
        medical_history.diagnosis = request.POST['diagnosis']
        medical_history.treatment_description = request.POST['treatment_description']
        medical_history.notes = request.POST['notes']
        medical_history.save()
        messages.success(request, 'Medical details updated successfully')
        return redirect('medical_history', patient_id=medical_history.patient.id)
    context = {
        'doctor': doctor,
        'appointment': appointment,
        'medical_history': medical_history
    }
    return render(request, 'doctorapp/updatemedicaldetails.html', context)

@doctor_required
def MedicalHistoryPatientList(request):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)
    patient_ids = appointments.values_list('patient', flat=True)
    patients = PatientProfile.objects.filter(id__in=patient_ids)
    return render(request, 'doctorapp/MedicalPatientList.html', {'patients': patients})

@doctor_required
def ViewMedicalHistory(request, patient_id):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    patient = get_object_or_404(PatientProfile, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient, doctor=doctor)
    medical_histories = MedicalHistory.objects.filter(patient=patient, doctor=doctor)
    appointment_histories = []
    for appointment in appointments:
        history = medical_histories.filter(appointment=appointment).first()
        prescriptions = Prescription.objects.filter(medical=history) if history else []
        appointment_histories.append({
            'appointment': appointment,
            'history': history,
            'prescriptions': prescriptions,
        })
    return render(request, 'doctorapp/MedicalHistory.html', {
        'patient': patient,
        'appointment_histories': appointment_histories,
    })

@doctor_required
def edit_prescription(request, appointment_id):
    if request.method == "POST":
        medication = request.POST.get('medication')
        dosage = request.POST.get('dosage')
        frequency = request.POST.get('frequency')
        medical_history = get_object_or_404(MedicalHistory, appointment__id=appointment_id)
        prescription, created = Prescription.objects.get_or_create(
            medical=medical_history,
            defaults={
                'patient': medical_history.patient,
                'doctor': medical_history.doctor,
                'medication': medication,
                'dosage': dosage,
                'frequency': frequency,
            }
        )
        if not created:
            prescription.medication = medication
            prescription.dosage = dosage
            prescription.frequency = frequency
            prescription.save()
        messages.success(request, "Prescription updated successfully!")
        return redirect('medical_history', patient_id=medical_history.patient.id)

@doctor_required
def view_prescriptions(request):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient')
    data = []
    for appointment in appointments:
        medical_history = MedicalHistory.objects.filter(appointment=appointment).first()
        prescriptions = Prescription.objects.filter(medical=medical_history) if medical_history else []
        data.append({
            'appointment': appointment,
            'medical_history': medical_history,
            'prescriptions': prescriptions,
        })
    return render(request,'doctorapp/eprescription.html',{'doctor': doctor,'data': data})

@doctor_required
def upload_article(request):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(DoctorProfile,id=doctor_id)
    if request.method == 'POST':
        articleform = HealthArticleForm(request.POST, request.FILES)
        if articleform.is_valid():
            article = articleform.save(commit=False)
            article.doctor = doctor
            article.save()
            messages.success(request,'New Article Uploaded Successfully')
            return redirect('articles')
        else:
            messages.error(request, "Error uploading article.")
    else:
        articleform = HealthArticleForm()
    return render(request,'doctorapp/new_article.html',{'articleform':articleform,'doctor':doctor})

@doctor_required
def send_to_pharmacy(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    existing_entry = PharmacyModel.objects.filter(prescription=prescription).exists()
    if existing_entry:
        messages.warning(request, "This prescription is already sent to the pharmacy.")
    else:
        PharmacyModel.objects.create(
            prescription=prescription,
            availability_status='In-stock',
        )
        messages.success(request, "Prescription sent to the pharmacy successfully.")
    return redirect('eprescriptions')






