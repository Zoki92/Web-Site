from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

from .models import CustomUser


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        if sociallogin.is_existing:
            return

        if 'email' not in sociallogin.account.extra_data:
            return

        try:
            email = sociallogin.account.extra_data['email'].lower()
            user = settings.CustomUser.objects.get(email__iexact=email)

        except CustomUser.DoesNotExist:
            return


        sociallogin.connect(request, user)


