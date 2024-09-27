from django.shortcuts import render, HttpResponse, redirect
import joblib
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views import View

model  = joblib.load('static/XGB_model.joblib')


@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def about_us(request):
    return render(request, 'about.html')

@login_required
def contact_us(request):
    return render(request, 'contact.html')

@login_required
def prediction(request):
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        sex = int(request.POST.get('sex'))
        bmi = int(request.POST.get('bmi'))
        children = int(request.POST.get('children', 0))  # Set default value to 0 if children is empty
        smoker = int(request.POST.get('smoker'))
        region = int(request.POST.get('region'))
        print(age, sex, bmi, children, smoker, region)
        
        pred = round(model.predict([[age, sex, bmi, children, smoker, region]])[0])
        print(pred)
        return render(request, 'prediction.html', {'pred': pred})
    else:
        return render(request, 'prediction.html')
    

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"{username} is now logged in.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            settings.MESSAGE_TAGS['error'] = 'Invalid username or password.'
            messages.error(request, "Invalid username or password.")
    elif request.method == 'GET':
        login_form = AuthenticationForm()
        
    return render(request, 'login.html', {'login_form': login_form})

class RegisterView(View):
    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'registration.html', {'register_form': register_form})
    
    def post(self, request):
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(request, f"{user.username} is now Registered in.")
            return redirect('home')
        else:
            settings.MESSAGE_TAGS['error'] = 'Invalid username or password.'
            messages.error(request, "Invalid username or password.")
            return render(request, 'registration.html', {'register_form': register_form})