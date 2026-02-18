from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/index.html')

@login_required
def profile(request):
    return render(request, 'main/profile.html')

def register(request):
    return render(request, 'main/registration.html')

def create_design_request(request):
    return render(request, 'main/create.html')


def is_admin(user):
    return user.is_superuser

