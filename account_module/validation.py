import re

from django.core.exceptions import ValidationError


def is_valid_iran_code(value):
    if not re.search(r'^\d{10}$', value): return False
    check = int(value[9])
    s = sum(int(value[x]) * (10 - x) for x in range(9)) % 11
    is_checked = check == s if s < 2 else check + s == 11
    if is_checked:
        return value
    raise ValidationError("کد ملی وارد شده معتبر نمیباشد")
