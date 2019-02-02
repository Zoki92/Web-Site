from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.views import PasswordChangeView, PasswordSetView
from .forms import CustomUserChangeForm, ProfileUpdateForm
from django.urls import reverse, reverse_lazy
from allauth.account.models import EmailAddress


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    email_address = EmailAddress.objects.filter(user=request.user)[0]

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'email_address' : email_address,

    }

    return render(request, 'account/profile.html', context)


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("profile")

login_after_password_change = login_required(MyPasswordChangeView.as_view())

class MyPasswordSetView(PasswordSetView):
    success_url = reverse_lazy("profile")

password_set = login_required(MyPasswordSetView.as_view())