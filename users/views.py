from django.contrib import messages
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserIsNotAuthenticated(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect('shop:flowers_list')


class LoginUser(SuccessMessageMixin, LoginView):
    template_name = 'user/login.html'
    success_message = 'Добро пожаловать на сайт!'

    def get_success_url(self):
        return reverse_lazy('shop:flowers_list')


class RegisterView(UserIsNotAuthenticated, CreateView):
    """
    Регистрация на сайте
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('shop:flowers_list')
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        # new_key = User.objects.make_random_password(length=6,
        #                                             allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        # new_user = form.save(commit=False)
        # new_user.verification_key = new_key
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm', kwargs={'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current().domain

        send_mail(
            subject='Подтвердите свой электронный адрес',
            message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return redirect('users:email_confirmation_sent/')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed/')
        else:
            return redirect('users:email_confirmation_failed/')

    # form.save()
    # return super().form_valid(form)


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


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
