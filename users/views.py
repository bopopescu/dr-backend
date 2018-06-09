from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from oauth2_provider.models import AccessToken
from braces.views import CsrfExemptMixin
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
from rest_framework.views import APIView
import json
from django.utils import timezone
from django.http import HttpResponseRedirect

from .serializers import UserSerializer
from .models import User
from mailserver import send_forgotpassword_mail

import hashlib
import random
import string
import datetime, time
# import requests


# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Register new User
    """
    print request.data
    if request.method == 'POST':
        if User.objects.filter(email=request.data['email']):
            print "user already exist"
            return Response(status=302, data={'error': 'user already exists'})
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid(raise_exception=True):
            # userSerializer.validated_data['is_active'] = True
            userSerializer.save()
        return Response(status=200, data=userSerializer.data)


# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def generateQr(request):
    print request.data
    randomstring=''.join(random.sample(string.lowercase+string.digits,5))
    stringhash=hashlib.md5(randomstring).hexdigest()
    currtime = time.time()
    timehash = hashlib.md5(str(currtime)).hexdigest()
    qrhash = stringhash+timehash
    qrhash_expiration=timezone.now()+timezone.timedelta(minutes=300)
    # user.otp=otp
    # user.otp_expiration=otp_expiration
    if request.method == 'POST':
        if User.objects.filter(email=request.data['email']):

            user=User.objects.get(email=request.data['email'])
            if user.qrhash:

                if timezone.now() <= user.qrhash_expiration:
                    print user.qrhash_expiration
                    print timezone.now()
                    return Response(status=200, data={'qrhash': user.qrhash})

                else:
                    user.qrhash = qrhash
                    user.qrhash_expiration = qrhash_expiration

                    user.save()

                    return Response(status=200, data={'qrhash': qrhash})
            else:

                user.qrhash = qrhash
                user.qrhash_expiration = qrhash_expiration

                user.save()

                return Response(status=200, data={'qrhash': qrhash})
        data = {}
        data['email'] = request.data['email']
        data['password'] = "batman25"
        print data
        userSerializer = UserSerializer(data=data)
        if userSerializer.is_valid(raise_exception=True):
            # userSerializer.validated_data['is_active'] = True
            userSerializer.save()
            user=User.objects.get(email=request.data['email'])
            user.qrhash = qrhash
            user.qrhash_expiration = qrhash_expiration
            user.save()
            print qrhash + " this is 2"
        return Response(status=200, data={'qrhash': user.qrhash})




@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])
def verifyemail(request):
    """
    User veryfying email
    """

    if request.method == 'GET':
        #needs email_token and password > updates user password on right token
        try:
            user=User.objects.get(otp=request.query_params['email_token'])
            print timezone.now()
            if timezone.now() <= user.otp_expiration:
              user.email_verified=True
              user.is_active=True
              user.otp_expiration=timezone.now() # expire the token
              user.save()

              return Response(status=200, data={"response":"Your email is successfully verified"})
            else:
              return Response(status=401, data={"error":"email token expired"})

        except User.DoesNotExist:
            return Response(status=401, data={'error': 'token invalid'})

        except Exception as e:
            return Response(status=400, data={'error': e.message})

    if request.method == 'POST':
        #checks if user exists if it does then send email with verification token again as well as increase the
        #expiration time by 5 hours does not generate new otp
        try:
            user=User.objects.get(email=request.data.get('email'))
            otp_expiration=timezone.now()+timezone.timedelta(minutes=300)
            user.otp_expiration=otp_expiration
            user.save()
            send_registration_mail(user.email,user.first_name,user.otp)

            return Response(status=200, data={"success":"true"})

        except User.DoesNotExist:
            return Response(status=404, data={'error': 'email doesnt exists'})

        except Exception as e:
            return Response(status=400, data={'error': e.message})

@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])
def forgotpasswordemail(request):

    """
    Forgot password api
    """

    if request.method == 'POST':

        try:

            user_email=request.data['user_email']
            user=User.objects.get(email=user_email)
            user_details=User.objects.filter(email=user_email)
            userSerializer = UserSerializer(user_details, many=True)
            user_name = userSerializer.data[0]['user_name']
            # print user_name
            randomstring=''.join(random.sample(string.lowercase+string.digits,5))
            hashstring=hashlib.md5(randomstring).hexdigest()
            otp = hashstring[:6]
            otp_expiration=datetime.datetime.now()+datetime.timedelta(minutes=10)
            print otp_expiration
            user.forget_otp=otp
            user.forget_otp_expiration=otp_expiration
            user.save()
            send_forgotpassword_mail(user_email,user_name,otp)

            return Response(status=200, data={"response":"OTP is sent to your email address"})
        except User.DoesNotExist:
            return Response(status=404, data={'error': 'email doesnt exists'})

        except Exception as e:
            return Response(status=400, data={'error': e.message})


@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])
def resetpassword(request):

    """
    Reset password api
    """

    try:
        forget_otp = request.data['forget_otp']
        user=User.objects.get(forget_otp=forget_otp)
        new_password = request.data['new_password']
        print timezone.now()
        if timezone.now() <= user.forget_otp_expiration:

          user.set_password(new_password)
          user.forget_otp_expiration=timezone.now() # expire the token
          user.save()

          return Response(status=200, data={"response":"Password is changed successfully"})
        else:
          return Response(status=401, data={"error":"otp token expired"})

    except User.DoesNotExist:
        return Response(status=401, data={'error': 'token invalid'})

    except Exception as e:
        return Response(status=400, data={'error': e.message})


class TokenView(APIView, CsrfExemptMixin, OAuthLibMixin):
    permission_classes = (permissions.AllowAny,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def issue_new_token(self, request, user, email):
        url, headers, body, status = self.create_token_response(request)
        data = json.loads(body)
        try:
            tokenObject = AccessToken.objects.get(token=data['access_token'])
        except:
            return Response(data=body, status=401)
        tokenObject.user = user
        print tokenObject.expires
        tokenObject.save()
        user_details=User.objects.filter(email=email)
        userSerializer = UserSerializer(user_details, many=True)
        data['email'] = email
        data['name'] = userSerializer.data[0]['user_name']
        data['role'] ={'admin':userSerializer.data[0]['is_admin'],
                'active':userSerializer.data[0]['is_active'],
                }
        return Response(data, status=status, headers=headers)

    def post(self, request):
        email = request.POST.get('email')
        try:
            if email is None:
                raise User.DoesNotExist
        except Exception as e:
            print e
            return Response(data={'error': e.message}, status=400)
        try:
            user = User.objects.get(email=email)
            user_details=User.objects.filter(email=email)
            userSerializer = UserSerializer(user_details, many=True)
            if user.is_active == False:
                return Response(status=404, data={'error': 'user not verified'})
            if not user.check_password(request.POST.get('password')):
                return Response(status=401, data={'error': 'incorrect password'})
            userToken = AccessToken.objects.filter(user=user)
            if userToken:
                if timezone.now() <= userToken[0].expires:
                    # print timezone.now() - timezone.timedelta(days=365)

                    # print timezone.now() + timezone.timedelta(minutes=598)
                    # print userToken[0].expires
                    # print timezone.now() + timezone.timedelta(minutes=598) <= userToken[0].expires
                    return Response(data={
                        'access_token': userToken[0].token,
                        'token_type': 'Bearer',
                        'avatar': userSerializer.data[0]['avatar'],
                        "email": userSerializer.data[0]['email'],
                        "name":userSerializer.data[0]['user_name'],
                        "scope": userToken[0].scope,
                        "role":{'admin':userSerializer.data[0]['is_admin'],
                                'active':userSerializer.data[0]['is_active']
                        },
                        "status":'200'
                    }, status=200)
                else:
                    AccessToken.delete(userToken[0])
                    return self.issue_new_token(request, user, email)
            else:
                return self.issue_new_token(request, user, email)
        except Exception as e:
            print e.message
            return Response(status=404, data={'error': e.message})

class TokenViewQr(APIView, CsrfExemptMixin, OAuthLibMixin):
    permission_classes = (permissions.AllowAny,)

    print "qrtokenview"
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def issue_new_token(self, request, user, email):
        url, headers, body, status = self.create_token_response(request)
        data = json.loads(body)
        try:
            tokenObject = AccessToken.objects.get(token=data['access_token'])
        except:
            return Response(data=body, status=401)
        tokenObject.user = user
        tokenObject.save()
        user = User.objects.get(email=email)
        user_details=User.objects.filter(email=email)

        user.ismobile_loggedin = True
        user.save()
        userSerializer = UserSerializer(user_details, many=True)
        data['email'] = email
        data['name'] = userSerializer.data[0]['user_name']
        data['role'] ={'admin':userSerializer.data[0]['is_admin'],
                'active':userSerializer.data[0]['is_active'],
                'supervisior':userSerializer.data[0]['is_supervisior']}
        return Response(data, status=status, headers=headers)

    def post(self, request):
        email = request.POST.get('email')
        try:
            if email is None:
                raise User.DoesNotExist
        except Exception as e:
            print e
            return Response(data={'error': e.message}, status=400)
        try:
            user = User.objects.get(email=email)
            user_details=User.objects.filter(email=email)
            userSerializer = UserSerializer(user_details, many=True)
            if user.is_active == False:
                return Response(status=404, data={'error': 'user not verified'})
            if not user.check_password("batman25"):
                return Response(status=401, data={'error': 'incorrect password'})
            userToken = AccessToken.objects.filter(user=user)
            print timezone.now()
            if not user.qrhash == request.POST.get('qrcode'):
                return Response(status=404, data={'error': 'Qrcode is not valid'})

            # if not timezone.now() >= user.qrhash_expiration:
            #     print user.qrhash
            #     print timezone.now()
            #     print
            #     return Response(status=404, data={'error': 'Qrcode is expired'})

            # if user.ismobile_loggedin and timezone.now() <= userToken[0].expires:
                # return Response(status=404, data={'error': 'You are already logged in any device'})

            if userToken:
                if timezone.now() <= userToken[0].expires:

                    user.ismobile_loggedin = True
                    user.save()
                    return Response(data={
                        'access_token': userToken[0].token,
                        'token_type': 'Bearer',
                        "email": userSerializer.data[0]['email'],
                        "name":userSerializer.data[0]['user_name'],
                        'avatar': userSerializer.data[0]['avatar'],
                        "scope": userToken[0].scope,
                        "role":{'admin':userSerializer.data[0]['is_admin'],
                                'active':userSerializer.data[0]['is_active'],

                        },
                        "status":'200'
                    }, status=200)
                else:
                    AccessToken.delete(userToken[0])
                    return self.issue_new_token(request, user, email)
            else:
                return self.issue_new_token(request, user, email)
        except Exception as e:
            print e.message
            return Response(status=404, data={'error': e.message})





class RevokeTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        token = AccessToken.objects.get(user=request.user)
        AccessToken.delete(token)
        return Response(status=200)
