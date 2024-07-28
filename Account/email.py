from django.conf import settings
from djoser.email import ActivationEmail, PasswordResetEmail


class AccountActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = settings.EMAIL_FRONTEND_DOMAIN
        context['site_name'] = settings.EMAIL_FRONTEND_SITE_NAME
        context['protocol'] = settings.EMAIL_FRONTEND_PROTOCOL
        return context


class AccountPasswordResetEmail(PasswordResetEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = settings.EMAIL_FRONTEND_DOMAIN
        context['site_name'] = settings.EMAIL_FRONTEND_SITE_NAME
        context['protocol'] = settings.EMAIL_FRONTEND_PROTOCOL
        return context
