#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_buff.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = "admin1"
    email = "admin1@test.com"
    password = "adminpassword1234"
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
    else:
        print(f"Superuser '{username}' already exists!")

if __name__ == '__main__':
    create_admin()
