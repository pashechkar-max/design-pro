from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DesignRequest
from django.contrib import messages

def is_admin(user):
    return user.is_superuser

def index(request):
    return render(request, 'main/index.html')

@login_required
def profile(request):
    return render(request, 'main/profile.html')

def register(request):
    return render(request, 'main/register.html')

def create_design_request(request):
    return render(request, 'main/create.html')

def my_requests(request):
    return render(request, 'main/my_requests.html')

@login_required
def delete_design_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user)

    if design_request.status != 'new':
        messages.error(request, "Эту заявку нельзя удалить, она уже в работе или выполнена.")
        return redirect('my_requests')

    if request.method == 'POST':
        design_request.delete()
        messages.success(request, "Заявка успешно удалена!")
        return redirect('my_requests')

    return render(request, 'main/delete_request.html', {'request_obj': design_request})



