from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, generate_new_password, EmailConfirmationSentView, EmailConfirmedView, \
    EmailConfirmationFailedView, UserConfirmEmailView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login/'),
    path('logout/', LogoutView.as_view(), name='logout/'),
    path('register/', RegisterView.as_view(), name='register/'),
    path('profile/', ProfileView.as_view(), name='profile/'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),


    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent/'),
    path('confirm/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed/'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed/'),

]
