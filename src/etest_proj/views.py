from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# '/'
def home(request):
    # If not logged, redirect to login
    # If logged, redirect to tests/home
    if request.user.is_authenticated:
        return redirect('/tests')
    else:
        return redirect('login')

# log out
def logout_view(request):
    logout(request)
    return redirect('login')

# login_view
def login_view(request):
    login_form = AuthenticationForm()
    
    context = {
        'form': login_form,
        'is_login': True
    }

    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            # Change to username or email
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('tests:index')
        else:
            context['error'] = 'Something went wrong. Please, check your email or your password'
            return render(request, 'auth/login.html', context)
    


    return render(request, 'auth/login.html', context)

