from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.core.urlresolvers import reverse
from django.contrib.auth import views as authViews
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

# from bot import bot
from account.forms import (UserLoginForm,
                           UserRegistrationForm,
                           UserEditForm,
                           ProfileEditForm,
                           MyPasswordChangeForm)
from account.models import Profile


def login_view(request):
    # bot.send_details(request, 'login page')
    title = "Login"
    if request.method == 'POST':
        try:
            next_url = request.GET['next']
        except Exception:
            next_url = reverse('main:display')

        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, "registration/login.html", {"form": form, "title": title})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.is_active = False
            user.save()
            new_user = authenticate(username=user.username, password=password)
            # login(request, new_user)
            Profile.objects.create(user=new_user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # from datetime import datetime, timedelta
            token = default_token_generator.make_token(new_user)
            str = 'برای تایید ایمیل خود روی لینک زیر کلیک کنید: \n'
            url = 'https://xtrader.ir/account/account-activation/confirm/' + uid.decode() + '/' + token
            send_mail('Xtrader تایید ایمیل', str + url, '', [user.email], fail_silently=False)

            # bot.send_message('some one new with username ' + user.username)
            return render(request, "account/register_done.html", {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def account_activation(request, uidb64=None, token=None):
    UserModel = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/Email_confirmed_done.html')
    else:
        return render(request, 'registration/Email_confirmed_notdone.html')


def logout_view(request):
    # bot.send_details(request, 'logout')
    logout(request)
    return redirect(reverse('main:index'))


@login_required
def edit(request):
    u = get_user_model().objects.filter(username=request.user).first()
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.account_profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت به روز رسانی شد.')
        else:
            pass
            messages.error(request, 'هنگام بروز رسانی پروفایل شما خطایی رخ داده است.')
    else:
        default_data = {'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email}
        user_form = UserEditForm(default_data, instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.account_profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form, 'username': request.user.username})

@sensitive_post_parameters()
@csrf_protect
@login_required
@authViews.deprecate_current_app
def password_change(request):
    return authViews.password_change(request, post_change_redirect='account:password_change_done',
                                     password_change_form=MyPasswordChangeForm,
                                     extra_context={'username': request.user.username})


@login_required
@authViews.deprecate_current_app
def password_change_done(request):
    return authViews.password_change_done(request, extra_context={'username': request.user.username})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'username': request.user.username})
