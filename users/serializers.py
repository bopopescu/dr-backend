from rest_framework import serializers

from .models import User
from .mailserver import send_verification_mail
import random
import string
import hashlib
import datetime
import smtplib
from django.conf import settings
import mailserver
import os
import subprocess


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'is_active', 'is_admin', 'email', 'phone','password','avatar']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
            user = User(**validated_data)
            user.set_password(validated_data['password'])

            randomstring=''.join(random.sample(string.lowercase+string.digits,5))

            otp=hashlib.md5(randomstring).hexdigest()
            otp_expiration=datetime.datetime.now()+datetime.timedelta(minutes=300)
            user.otp=otp
            user.otp_expiration=otp_expiration
            # execfile("mailserver.py")
            print "start"
            # process = subprocess.call('python users/mailserver.py', shell=True)
            print "deepak korku"
            send_verification_mail(user.email,user.user_name,user.otp)
            user.save()
            return user
