from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserKeyForm
from users.models import User


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    key_field = forms.CharField(max_length=6)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse_lazy('flowers:flowers_list')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:key_verification')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def form_valid(self, form):
        new_key = User.objects.make_random_password(length=6,
                                                    allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        new_user = form.save()
        new_user.verification_key = new_key

        send_mail(
            subject='Регистрация на сайте',
            message=f'Для регистрации вам направлен ключ {new_key}, введите его в поле "Ключ" в форме Авторизации',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )

        form.save()
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('shop:flowers_list/')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = User.objects.make_random_password(length=10,
                                                     allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')

    send_mail(
        subject='вы сменили пароль',
        message=f'Ваш новый пароль:{new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],

    )

    request.user.set_password(new_password)
    request.user.save()

    return redirect(reverse('shop:flowers_list/'))


def key_verification(request):
    if request.method == 'POST':
        form = UserKeyForm(request.POST)
        if form.is_valid():
            email_key = form.cleaned_data['verification_key']
            print(email_key)
            bd_key = (User.objects.all())
            print(bd_key)


    else:
        form = UserKeyForm()

    return render(request, 'users/key_verification.html', {'form': form, 'key': 'verification_key'})
