# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username
        try:
            # メールアドレスでユーザーを取得
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.password == password:  # パスワードのチェック（ハッシュ化されている場合は適切な方法で比較）
            return user
        return None