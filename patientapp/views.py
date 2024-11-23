from django.shortcuts import render,redirect,get_object_or_404
from adminapp.models import *
from adminapp.forms import *
from django.contrib import messages
from patientapp.forms import *
from django.conf import settings
from django.urls import reverse
import stripe
from django.http import HttpResponseRedirect
from doctorapp.models import *

def patient_dashboard(request):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    patient = get_object_or_404(PatientProfile,id=patient_id)
    facilities = Facility.objects.all()
    patients = PatientProfile.objects.all()
    doctors = DoctorProfile.objects.all()
    appointments = Appointment.objects.filter(patient=patient)
    total_facilities = facilities.count()
    total_patients = patients.count()
    total_doctors = doctors.count()
    total_facilities = facilities.count()
    scheduled_appointments = Appointment.objects.filter(status='Scheduled',patient=patient)
    return render(request,'patientapp/dashboard.html',{
        'total_facilities': total_facilities,
        'total_doctors':total_doctors,
        'total_patients': total_patients,
        'appointments' : appointments,
        'patient': patient,
        'scheduled_appointments':scheduled_appointments
    })

def new_appointment(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    patient = get_object_or_404(PatientProfile, id=patient_id)

    # Extract `appointment_id` from query parameters if present
    appointment_id = request.GET.get('appointment_id')

    if request.method == 'POST':
        appointmentform = BookAppointment(request.POST)
        if appointmentform.is_valid():
            appointment = appointmentform.save(commit=False)
            appointment.patient = patient
            appointment.status = 'Pending Payment'
            appointment.save()
            appointment_id = appointment.id
            print(appointment_id)
            messages.success(request, 'Appointment created successfully')
            return redirect('checkout_session', appointment_id=appointment_id)
        else:
            messages.error(request, "Error creating appointment. Please correct the errors below.")
    else:
        appointmentform = BookAppointment()

    doctors = DoctorProfile.objects.all()
    context = {
        'appointmentform': appointmentform,
        'doctors': doctors,
        'patient': patient,
        'appointment_id': appointment_id,
    }
    return render(request, 'patientapp/newappointment.html', context)


def checkout_session(request, appointment_id):
    try:
        # Fetch appointment
        appointment = get_object_or_404(Appointment, id=appointment_id)
        print("Fetched appointment:", appointment)

        # Ensure the appointment is pending payment
        if appointment.status != 'Pending Payment':
            messages.warning(request, 'This appointment cannot be paid for at this time.')
            return redirect('pat_appointments')

        # Set Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print("Stripe API Key set.")

        try:
            line_item = {
                'price_data': {
                    'currency': 'INR',
                    'unit_amount': 500 * 100,  # Amount in paise
                    'product_data': {
                        'name': f'Appointment with {appointment.doctor.name}',
                    },
                },
                'quantity': 1,
            }
            print("Line item created:", line_item)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[line_item],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success', args=[appointment_id])),
                cancel_url=request.build_absolute_uri(reverse('pat_appointments')),
            )
            print("Stripe Checkout Session created:", checkout_session)

            Payment.objects.create(
                patient=appointment.patient,
                doctor=appointment.doctor,
                appointment=appointment,
                amount=500.00,
                stripe_payment_id=checkout_session.id,
                status='pending',
            )
            print("Payment record created.")

            print("Redirecting to:", checkout_session.url)
            return redirect(checkout_session.url)

        except Exception as e:
            print("Stripe session creation error:", e)
            messages.error(request, 'Error creating payment session. Please try again.')
            return redirect('pat_appointments')

    except Exception as e:
        print("Error in checkout_session function:", e)
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('pat_appointments')



def payment_success(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)
    payment = get_object_or_404(Payment, appointment=appointment)
    payment.status = 'Paid'
    payment.save()
    appointment.status = 'Scheduled'
    appointment.save()

    messages.success(request, 'Payment successful! Your appointment is confirmed.')
    return redirect('pat_appointments')



def appointment_detail(request, id):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    appointment = get_object_or_404(Appointment,id=id)
    return render(request,'patientapp/appointmentdetails.html',{'appointment':appointment})

def edit_appointment(request, id):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
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
        return redirect('pat_appointment_detail', id=appointment.id)
    doctors = DoctorProfile.objects.all()
    return render(request, 'patientapp/appointmentdetails.html', {
        'appointment': appointment,
        'doctors': doctors
    })

def appointments(request):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    patient = PatientProfile.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request,'patientapp/appointments.html',{'appointments' : appointments})

def MedicalHistoryList(request):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    patient = get_object_or_404(PatientProfile, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    doctor_ids = appointments.values_list('doctor', flat=True)
    doctors = DoctorProfile.objects.filter(id__in=doctor_ids)

    return render(request, 'patientapp/MedicalHistoryList.html', {'doctors': doctors})

def View_Medical(request, doctor_id):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    patient = get_object_or_404(PatientProfile, id=patient_id)

    # Fetch appointments and corresponding medical histories
    appointments = Appointment.objects.filter(patient=patient, doctor=doctor)
    medical_histories = MedicalHistory.objects.filter(patient=patient, doctor=doctor)

    # Map medical history and prescriptions to corresponding appointments
    appointment_histories = []
    for appointment in appointments:
        history = medical_histories.filter(appointment=appointment).first()
        prescriptions = Prescription.objects.filter(medical=history) if history else []
        appointment_histories.append({
            'appointment': appointment,
            'history': history,
            'prescriptions': prescriptions,
        })

    return render(request, 'patientapp/MedicalHistory.html', {
        'doctor': doctor,
        'appointment_histories': appointment_histories,
    })

def ViewPrescriptions(request):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    # Get the doctor profile
    patient = get_object_or_404(PatientProfile, id=patient_id)

    # Fetch appointments for the logged-in doctor
    appointments = Appointment.objects.filter(patient=patient).select_related('doctor')

    data = []
    for appointment in appointments:
        medical_history = MedicalHistory.objects.filter(appointment=appointment).first()
        prescriptions = Prescription.objects.filter(medical=medical_history) if medical_history else []

        data.append({
            'appointment': appointment,
            'medical_history': medical_history,
            'prescriptions': prescriptions,
        })

    return render(
        request,
        'patientapp/eprescription.html',
        {
            'patient': patient,
            'data': data,  # Pass combined data
        },
    )

def view_profile(request):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    patient = get_object_or_404(PatientProfile, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    medical_history = MedicalHistory.objects.filter(patient=patient)
    prescription = Prescription.objects.filter(patient=patient)

    return render(request, 'patientapp/view_profile.html', {
        'patient': patient,
        'appointments': appointments,
        'medical_history': medical_history,
        'prescription': prescription
    })

def edit_profile(request):

    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')
    patient = get_object_or_404(PatientProfile, id=patient_id)

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient details updated successfully.")
            return redirect('view_profile')
    else:
        form = PatientProfileForm(instance=patient)

    return render(request, 'patientapp/edit_profile.html', {'form': form, 'patient': patient})