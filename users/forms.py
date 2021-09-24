from django.contrib.auth.forms import AuthenticationForm
from users.models import User

class userLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('login', 'password')
