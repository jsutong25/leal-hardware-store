from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered successfully. You can now login.')
            form = CreateUserForm()
            return redirect('user-login')
        else:
            messages.error(request, 'Registration failed. Please try again.')
            return redirect('user-register')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('user-login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(self.next_page)

def profile(request):
    return render(request, 'user/profile.html')

def profile_edit(request):
    if request.method == 'POST':
        # Instance fills the form out with the current info
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = { 
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_edit.html', context)