import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediplant.settings.dev')  # نام پروژه را بررسی کنید
django.setup()

from account.models import User
from doctor.models import Doctor, DockterBranch, DocktorPhone
from faker import Faker
import random

fake = Faker()
branches = list(DockterBranch.objects.all())

for _ in range(10):
    user = User.objects.create_user(
        phone=fake.unique.phone_number(),
        password="Test@1234"
    )
    user.user_name = fake.name()  # مقداردهی بعد از ایجاد کاربر
    user.save()

    doctor = Doctor.objects.create(
        user=user,
        branch=random.choice(branches) if branches else None,
        address=fake.address(),
        state=random.choice([0, 1, 2, 3, 4]),
        description=fake.text(),
        id_active=True,
        register_time=random.randint(1, 12),
        responsiveness=random.choice([0, 1, 2, 3]),
        postal_code=fake.postcode(),
        shaba=fake.bban(),
    )

    DocktorPhone.objects.create(
        doctor=doctor,
        phone=fake.phone_number()
    )

    print(f"Created Doctor: {user.user_name} - {user.phone}")
