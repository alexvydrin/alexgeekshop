from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def login(request):
    title = 'вход'
    login_form = ShopUserLoginForm(data=request.POST)
    _next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    message = ""
    message_link = ""
    if 'message_link' in request.session:
        if request.session['message_link']:
            message = f"Вам выслано сообщение на почту для подтверждения.\n"
            message += f"Так как сайт демонстрационный, то ссылку для подтверждения выведем здесь:\n"
            message_link = request.session['message_link']
            del request.session['message_link']

    content = {
        'title': title,
        'login_form': login_form,
        'next': _next,
        'message': message,
        'message_link': message_link,
    }

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            # return HttpResponseRedirect(reverse('auth:login'))
            send_ok, message_link = send_verify_mail(user)
            if send_ok:
                print('сообщение подтверждения отправлено')
                request.session['message_link'] = message_link
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                request.session['message_link'] = False
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            register_form = ShopUserRegisterForm()
            # content = {'title': title, 'register_form': register_form}
            # return render(request, 'authapp/register.html', content)
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}
    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(f'success - activation user: {user}')
            return render(request, 'authapp/verification.html', {'user': user})
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html', {'user': None})
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main'))


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'

    message_link = f"{settings.DOMAIN_NAME}{verify_link}"

    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} '
    message += f'перейдите по ссылке:\n{message_link}\n'

    # Вернём еще второе значение - ссылку для перехода - будем выводить её в отладочных целях
    # чтобы легче было залогиниться при тестировании сайта
    return \
        send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False), \
        message_link
