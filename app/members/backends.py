import json

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect

User = get_user_model()


class FacebookBackend:
    def authenticate(self, request, facebook_request_token):
        api_base = 'https://graph.facebook.com/v3.2'
        api_get_access_token = f'{api_base}/oauth/access_token'
        api_me = f'{api_base}/me'
        code = facebook_request_token

        params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': 'http://localhost:8000/members/facebook-login/',
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': code,
        }
        response = requests.get(api_get_access_token, params)
        data = response.json()
        access_token = data['access_token']

        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name',
                'last_name',
            ]),
        }
        response = requests.get(api_me, params)
        data = response.json()
        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']

        try:
            user = User.objects.get(username=facebook_id)
            # update_or_create 메서드를 사용하면 더 편하다.
            user.last_name = last_name
            user.first_name = first_name
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                first_name=first_name,
                last_name=last_name,
                provider='facebook',
            )
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
