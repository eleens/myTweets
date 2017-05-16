from django.contrib.auth.hashers import check_password
from user_profile.models import User

class KeystoneBackend(object):
    def authenticate(self, username=None, password=None):
        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
                return None
            if user:
                if user.password == password:
                    return user
                else:
                    return None
        else:
            return None

    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None
