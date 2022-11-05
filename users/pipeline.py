from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from users.models import UserProfile, User


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'country',
                                     'photo')), access_token=response['access_token'],
                    v=5.131)), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass

    if data['about']:
        user.userprofile.about = data['about']

    if data['country']:
        user.userprofile.language = data['country']['title']

    if data['photo']:
        user.userprofile.photo = data['photo']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()


    if response['email'] and not User.objects.filter(email=response['email']).exists():
        user.email = response['email']

    age = timezone.now().date().year - bdate.year
    user.age = age
    if age < 18:
    # if age < 100:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VK0Auth2')
    user.save()
