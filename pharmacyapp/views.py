from django.shortcuts import render,redirect,get_object_or_404
from pharmacyapp.models import *
from adminapp.models import *
from doctorapp.models import *
from functools import wraps
from accountsapp.views import *

def pharm_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('pharmacy_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@pharm_required
def pharmacy_list(request):
    pharmacy_list = PharmacyModel.objects.all()
    return render(request, 'pharmacyapp/Pharmacyview.html', {'pharmacy_list': pharmacy_list})

@pharm_required
def update_status(request, item_id):

    item = get_object_or_404(PharmacyModel, pk=item_id)
    if request.method == "POST":
        status = request.POST.get('status')
        item.availability_status = status
        item.save()
        return redirect('pharmacy_list')
    return render(request,'pharmacyapp/update_status.html',{'item':item})

