from django.contrib.auth.mixins import UserPassesTestMixin

from account_module.models import User


class JustSuperUser(UserPassesTestMixin):
    def test_func(self):
        user: User = self.request.user
        if user.is_authenticated and user.is_superuser:
            return True
        return False
