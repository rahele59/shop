import random
from datetime import datetime, timedelta
import hashlib

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.models import User

from utils.constant import TOKEN_USER, SUBJECT_FOR_FORGET_PASSWORD, KAVE_TEMPLATE
from utils.utils import send_email, send_sms
from .models import User as MyUser, ForgetPassword


# Create your views here.

class Register(APIView):

    @staticmethod
    def post(request):
        # اگر پارامترهای get ارسال شده بود
        # query_params = request.query_params
        data = request.data
        # ما در این قسمت با کلیدهای موجود اطلاعات کاربران را دریافت می کنیم
        username = data["user_name"]
        password = data["password"]
        email = data["email"]
        # با سه پارامتر بالا میتوانم یوزر استاندارد جنگو بسازم
        phone = data["phone"]
        name = data["name"]
        profile_image = data["profile_image"]
        token = data["token"]

        if token == TOKEN_USER:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            elif MyUser.objects.filter(phone=phone).exists():
                return JsonResponse({'error': 'Phone already exists'}, status=400)
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user2 = MyUser.objects.create(name=name, user_name=username, phone=phone, email=email,
                                          profile_image=profile_image)
                return JsonResponse({'status': 'کاربر با موفقیت اضافه شد'} ,status=201)
        else:
            return JsonResponse({'error': 'token not valid'}, status=400)


class Login(APIView):

    @staticmethod
    def post(request):
        data = request.data
        if data['token'] == TOKEN_USER:
            if 'phone' in data:
                phone = data['phone']
            else:
                phone = ""
            email = data['email'] if 'email' in data else ""
            password = data['password']
            # در این قسمت من ایمیل کاربر را از دیتابیس خودم استخراج  می کنم
            if phone != "" and email == "":
                username = MyUser.objects.get(phone=phone).user_name
            else:
                username = MyUser.objects.get(email=email).user_name

            user = authenticate(request, username=username, password=password)
            if user is not None:
                #login()
                user = MyUser.objects.get(user_name=username)
                print(datetime.now())
                mystring =username + str(datetime.now())
                sha1_object = hashlib.sha1()
                sha1_object.update(mystring.encode('utf-8'))
                sha1_hash = sha1_object.hexdigest()
                user.token = sha1_hash
                user.save()

                return JsonResponse({'status': 'لاگین شدید!', 'token':sha1_hash}, status=200)

            else:
                return JsonResponse({'status': 'چنین کاربری با این مشخصات وجود ندارد'}, status=400)
        else:
            return JsonResponse({'error': 'token not valid'}, status=400)

class ForgetPass(APIView):

    @staticmethod
    def post(request):
        data = request.data
        if data['token'] == TOKEN_USER:
            phone = data['phone'] if 'phone' in data else ""
            email = data['email'] if 'email' in data else ""
            random_code = random.randint(10000, 99999)
            fg_password = ForgetPassword.objects.create(phone=phone, email=email, code=random_code)
            if phone != "":
                #send sms
                send_sms(to=phone,token=random_code,template=KAVE_TEMPLATE)
                return JsonResponse({'status':"پیامک فعال سازی برای شما ارسال شد."}, status=200)
            else:
                # send_email
                send_email(email, SUBJECT_FOR_FORGET_PASSWORD, f"کد فراموشی شما برابر است با{random_code}")
                return JsonResponse({'status': "ایمیل فعال سازی برای شما ارسال شد"}, status=200)
        else:
            return JsonResponse({'error': 'token not valid'}, status=400)


class UpdatePass(APIView):
    @staticmethod
    def post(request):
        data = request.data
        phone = data['phone'] if 'phone' in data else ""
        email = data['email'] if 'email' in data else ""
        password = data['password']
        code = data['code']
        if data['token'] == TOKEN_USER:
            current_time = datetime.now()
            time_minus_2_minutes = current_time - timedelta(minutes=2)
            fp_user = ForgetPassword.objects.filter((Q(phone=phone, code=code) | Q(email=email, code=code)) &
                                                    Q(time_created__gt=time_minus_2_minutes))

            if fp_user.exists():
                fp_user.delete()
                username = MyUser.objects.get(Q(phone=phone) | Q(email=email)).user_name
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                return JsonResponse({'status': 'پسورد شما با موفقیت تغییر کرد'}, status=200)
            else:
                return JsonResponse({'status': 'کد فعال سازی شما صحیح نیست یا زمان استفاده آن از دو دقیقه گذشته است'}, status=400)
        else:
            return JsonResponse({'error': 'token not valid'}, status=400)



class UpdateProfile(APIView):

    @staticmethod
    def post(request, ):
        data = request.data
        # ما در این قسمت با کلیدهای موجود اطلاعات کاربران را دریافت می کنیم
        username = data['user_name']
        name = data['name']
        profile_image = data['profile_image']
        token_login = data['token_login'] if 'token_login' in data else "fake"
        token = data['token']
        if token == TOKEN_USER:
            user = MyUser.objects.filter(token=token_login)
            if user.exists():
                user.update(name=name, profile_image=profile_image, user_name=username)
                return JsonResponse({'status': 'تغییرات با موفقیت اعمال شد'}, status=200)
            else:
                return JsonResponse({'error': 'خطا در اعتبارسنجی لطفا مجدد لاگین شوید'}, status=400)
        else:
            return JsonResponse({'error': 'token not valid'}, status=400)