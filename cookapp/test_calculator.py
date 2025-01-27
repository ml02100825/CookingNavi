from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Familymember

User = get_user_model()

class FamilyMemberModelTest(TestCase):

    def setUp(self):
        """テスト用のユーザーと家族メンバーのセットアップ"""
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="securepassword",
            name="Test User"
        )

        self.family_member = Familymember.objects.create(
            family_name="山田花子",
            family_gender="F",
            family_age="2010-05-20",
            family_height=150.5,
            family_weight=45.0,
            user=self.user
        )

    def test_familymember_creation(self):
        """家族メンバーが正常に作成されるか確認"""
        family = Familymember.objects.get(family_name="山田花子")
        self.assertEqual(family.family_name, "山田花子")
        self.assertEqual(family.family_gender, "F")
        self.assertEqual(family.family_age, "2010-05-20")
        self.assertEqual(family.family_height, 150.5)
        self.assertEqual(family.family_weight, 45.0)
        self.assertEqual(family.user, self.user)

    def test_familymember_str_representation(self):
        """家族メンバーの文字列表現（str）が正しいか確認"""
        self.assertEqual(str(self.family_member.family_name), "山田花子")

    def test_familymember_user_relationship(self):
        """家族メンバーが正しいユーザーに関連付けられているか確認"""
        self.assertEqual(self.family_member.user.email, "testuser@example.com")

    def test_familymember_update(self):
        """家族メンバー情報の更新テスト"""
        self.family_member.family_height = 155.0
        self.family_member.save()
        updated_member = Familymember.objects.get(family_name="山田花子")
        self.assertEqual(updated_member.family_height, 155.0)

    def test_familymember_deletion(self):
        """家族メンバーの削除テスト"""
        self.family_member.delete()
        with self.assertRaises(Familymember.DoesNotExist):
            Familymember.objects.get(family_name="山田花子")
