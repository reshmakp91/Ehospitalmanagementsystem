from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from adminapp.forms import PatientProfileForm, DoctorProfileForm
from doctorapp.views import *
from adminapp.views import *
from accountsapp.forms import *
from doctorapp.models import *
from adminapp.models import *
from django.contrib import messages

def patient_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = PatientProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  # Ensures hashing
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to the login page or another view
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserRegistrationForm()
        profile_form = PatientProfileForm()

    return render(request, 'accountsapp/register_patient.html', {'user_form': user_form, 'profile_form': profile_form})

def doctor_register(request):

    selected_facility = None
    if request.method == 'POST':

        selected_facility = request.POST.get('facility')
        profile_form = DoctorProfileForm(request.POST, request.FILES, selected_facility=selected_facility)
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # Save user form with hashed password
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            # Save the DoctorProfile instance linked to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Registration successful!")
            return redirect('login')
        else:
            print(profile_form.errors)
            print(user_form.errors)

    else:
        profile_form = DoctorProfileForm()
        user_form = UserRegistrationForm()

    facilities = Facility.objects.all()
    return render(
        request,
        'accountsapp/register_doctor.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'facilities': facilities,
            'selected_facility': selected_facility,
        }
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_check = User.objects.get(username=username)
            print("User found:", user_check)
            if not user_check.is_active:
                messages.error(request, 'This account is inactive.')
                return render(request, 'accountsapp/login.html')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accountsapp/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'patientprofile'):
                request.session['patient_id'] = user.patientprofile.id
                request.session['username'] = username
                messages.success(request, "Login successful!")
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctorprofile'):
                request.session['doctor_id'] = user.doctorprofile.id
                request.session['username'] = username
                messages.success(request, "Login successful!")
                return redirect('doctor_dashboard')
            elif hasattr(user, 'adminprofile'):
                request.session['admin_id'] = user.adminprofile.id
                request.session['username'] = username
                print("Admin session set:", request.session['admin_id'])
                messages.success(request, "Login successful!")
                return redirect('admin_dashboard')
            elif hasattr(user, 'pharmacyprofile'):
                request.session['pharmacy_id'] = user.pharmacyprofile.id
                request.session['username'] = username
                messages.success(request, "Login successful!")
                return redirect('pharmacy_list')
            else:
                messages.error(request, 'No role assigned.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        print("GET request - rendering login page")
    return render(request, 'accountsapp/login.html')


def user_logout(request):

    logout(request)
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    elif 'patient_id' in request.session:
        del request.session['patient_id']
    elif 'admin_id' in request.session:
        del request.session['admin_id']
    elif 'pharmacy_id' in request.session:
        del request.session['pharmacy_id']
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def dashboard_redirect(request):

    if request.user.is_authenticated:

        if hasattr(request.user, 'doctorprofile'):
            return redirect('doctor_dashboard')
        elif hasattr(request.user, 'patientprofile'):
            return redirect('patient_dashboard')
        elif hasattr(request.user, 'adminprofile'):
            return redirect('admin_dashboard')
        elif hasattr(request.user, 'pharmacyprofile'):
            return redirect('pharmacy_list')
        else:
            return redirect('home')
    return redirect('login')

def home(request):

    return render(request,'accountsapp/index.html')

def articles_list(request):

    articles = HealthArticle.objects.all()
    return render(request, 'accountsapp/Articles.html', {'articles': articles})


def read_Article(request,article_id):

    article = get_object_or_404(HealthArticle,id=article_id)
    return render(request,'accountsapp/HealthArticle.html',{'article':article})


def view_facilities(request):

    facilities = Facility.objects.all()
    return render(request, 'accountsapp/facilities.html', {'facilities': facilities})

def view_facility_detail(request, facility_id):

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
    return render(request, 'accountsapp/facility_detail.html', context )

def view_doctors(request):

    doctors = DoctorProfile.objects.all()
    departments = DEPARTMENT_CHOICES
    facilities = Facility.objects.all()
    return render(request,'accountsapp/doctors.html', {'doctors':doctors, 'departments' : departments,'facilities': facilities})