# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# models.pyで定義したUserをインポート
from .models import User

class CustomUserCreationForm(UserCreationForm) :
    model = User
    fields = ("username",'mailaddress', 'password1', 'password2', 'height', 'weight', 'allergys', 'age','gender')
    
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User