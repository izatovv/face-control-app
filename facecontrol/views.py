from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import is_ajax, classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from main.models import Profile


def login_view(request):
    return render(request, 'main/login.html')


def register_view(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return render(request, 'main/register.html')

        user = User.objects.create_user(username=username, password=password)
        first_name = full_name.split(' ')[0] if len(full_name.split(' ')) > 0 else ''
        last_name = full_name.split(' ')[1] if len(full_name.split(' ')) > 1 else ''
        user.first_name = first_name
        user.last_name = last_name

        user.set_password(password)
        user.save()

        profile = Profile.objects.get(user=user)
        profile.bio = f'Full name is: {full_name}'
        profile.photo = photo
        profile.save()

        return redirect('login')

    return render(request, 'main/register.html')


def logout_view(request):
    auth.logout(request)
    return redirect('login')


@login_required
def home_view(request):
    profile = Profile.objects.get(user=request.user)
    if not profile:
        Profile.objects.create(user=request.user)

    context = {
        'profile': profile,
        'empty_fields': profile.empty_fields(),
        'completion_percentage': int(100 - (profile.empty_fields() / 5 * 100)),
        'user_count': User.objects.count()
    }

    return render(request, 'main/profile.html', context)


@login_required
def edit_profile_view(request):
    profile = Profile.objects.filter(user=request.user.id).first()

    # POST DATA: Profile contacts
    if request.method == 'POST' and 'first_name' in request.POST:
        photo = request.FILES.get('avatar')
        first_name = request.POST.get('first_name')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')

        if not first_name:
            messages.error(request, 'First name is required.')
        else:
            if photo:
                profile.photo = photo
            profile.phone_number = phone_number
            profile.country = country
            profile.save()

            User.objects.filter(id=request.user.id).update(
                first_name=first_name
            )

        return redirect('edit_profile')

    # POST DATA: Change Email contacts
    if request.method == 'POST' and 'new_email' in request.POST:
        new_email = request.POST.get('new_email')
        confirm_password = request.POST.get('confirm_password')

        print("new_email", new_email)
        print("confirm_password", confirm_password)

        if profile.user.check_password(confirm_password):
            # Check if email is already in use by another user
            if User.objects.filter(Q(email=new_email) & ~Q(id=request.user.id)).exists():
                messages.error(request, 'Email address already in use.')
            else:
                User.objects.filter(id=request.user.id).update(email=new_email)
        else:
            messages.error(request, 'Invalid password')

        return redirect('edit_profile')

    # POST DATA: Change Password contacts
    if request.method == 'POST' and 'new_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if profile.user.check_password(current_password):
            user = User.objects.get(id=request.user.id)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # update session
        else:
            messages.error(request, 'Invalid password.')

        return redirect('edit_profile')

    context = {
        'profile': profile,
        'empty_fields': profile.empty_fields() if profile else 0,
        'completion_percentage': int(100 - (profile.empty_fields() / 5 * 100)) if profile else 0,
        'user_count': User.objects.count()
    }

    return render(request, 'main/edit_profile.html', context)


def find_user_view(request):
    if is_ajax(request):
        try:
            photo = request.POST.get('photo')
            _, str_img = photo.split(';base64')

            decoded_file = base64.b64decode(str_img)

            x = Log()
            x.photo.save('upload.png', ContentFile(decoded_file))
            x.save()

            res = classify_face(x.photo.path)
            if res:
                user_exists = User.objects.filter(username=res).exists()
                if user_exists:
                    user = User.objects.get(username=res)
                    profile = Profile.objects.get(user=user)
                    x.profile = profile
                    x.save()

                    auth.login(request, user)
                    return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('login')
