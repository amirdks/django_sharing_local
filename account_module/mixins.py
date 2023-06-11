from django.contrib.auth.mixins import UserPassesTestMixin

from account_module.models import User


class JustSuperUser(UserPassesTestMixin):
    def test_func(self):
        user: User = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.administrative_department_head.exists():
                return True
            else:
                return False
        else:
            return False
