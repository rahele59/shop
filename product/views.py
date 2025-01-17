import json
import token

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render

from product.models import *
from utils.constant import TOKEN_USER


# Create your views here.
class HomeView(APIView):
    @staticmethod
    def get(request):
        token = request.GET.get('token')
        if token == TOKEN_USER:
            #top banner
            # category
            is_banner = Product.objects.filter(is_banner=1)
            data = ""
            if is_banner.exists():
                product = is_banner.first()
                banner = ProductImage.objects.filter(product=product)
                banner = banner.first()
                data = {
                    'banner': banner.banner,
                    'product_id': banner.product_id,
                }

            return JsonResponse({'top_banner': data}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'token not valid'}, status=status.HTTP_401_UNAUTHORIZED)


class AddCategory(APIView):
    @staticmethod
    def post(request):
        data = request.data
        token = data.get('token')
        name = data.get('name')
        image = data.get('image')
        if token == TOKEN_USER:
            category = Category.objects.create(name=name, image=image)
            if category:
                return JsonResponse({'status': 'دسته بندی جدید ایجاد شد', 'category': category.name},
                                    status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'مشکل در ثبت دسته بندی'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'توکن صحیح نیست'},status=status.HTTP_401_UNAUTHORIZED)


class AddProduct(APIView):
    @staticmethod
    def post(request):
        data = request.data
        token = data.get('token')
        name = data.get('name')
        price = data.get('price')
        final_price = data.get('final_price')
        banners = data.get('banners')
        description = data.get('description')
        user_id = int(data.get('user_id'))
        category_id = int(data.get('category_id'))

        if token == TOKEN_USER:
            product = Product.objects.create(name=name, price=price, final_price=final_price,
                                                 description=description,
                                                 user_id=user_id, category_id=category_id)
            if product:
                json_string = banners

                data = json.loads(json_string)
                image = data['image'] if 'image' in data else None
                video = data['video'] if 'video' in data else None
                banner = data['banner'] if 'banner' in data else None
                image2 = data['image2'] if 'image2' in data else None
                image3 = data['image3'] if 'image3' in data else None
                image4 = data['image4'] if 'image4' in data else None
                image5 = data['image5'] if 'image5' in data else None
                image6 = data['image6'] if 'image6' in data else None
                image7 = data['image7'] if 'image7' in data else None

                product_image = ProductImage.objects.create(product=product, image=image, video=video,
                                                            banner=banner,
                                                            image2=image2, image3=image3, image4=image4,
                                                            image5=image5, image6=image6, image7=image7)
                return JsonResponse({'status': 'محصول با موفقیت اضافه شد', 'product': product.name}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error':'مشکل در ثبت دسته بندی' , 'product': product}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'توکن صحیح نیست'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateProduct(APIView):
    @staticmethod
    def post(request):
        data = request.data
        token = data.get('token')
        name = data.get('name')
        price = data.get('price')
        final_price = data.get('final_price')
        banners = data.get('banners')
        description = data.get('description')
        user_id = int(data.get('user_id'))
        category_id = int(data.get('category_id'))
        product_id = data.get('product_id')

        if token == TOKEN_USER:
            product = Product.objects.filter(id=product_id, user_id=user_id)
            if product.exists():
                product = product.first()
                product.name = name
                product.price = price
                product.final_price = final_price
                product.description = description
                product.category_id = category_id
                product.save()


                json_string = banners

                data = json.loads(json_string)
                image = data['image'] if 'image' in data else None
                video = data['video'] if 'video' in data else None
                banner = data['banner'] if 'banner' in data else None
                image2 = data['image2'] if 'image2' in data else None
                image3 = data['image3'] if 'image3' in data else None
                image4 = data['image4'] if 'image4' in data else None
                image5 = data['image5'] if 'image5' in data else None
                image6 = data['image6'] if 'image6' in data else None
                image7 = data['image7'] if 'image7' in data else None

                product_image = ProductImage.objects.filter(product=product).update(product=product, image=image,
                                                                                    video=video, banner=banner,
                                                                                    image2=image2, image3=image3,
                                                                                    image4=image4,
                                                                                    image5=image5, image6=image6,
                                                                                    image7=image7)
                return JsonResponse({'status':'محصول شما به روز شد', 'product': product.name}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'مشکل در ثبت دسته بندی'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'توکن صحیح نیست'}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteProduct(APIView):
    @staticmethod
    def delete(request):
        data = request.data
        product_id = data.get('product_id')
        token = data.get('token')

        if token == TOKEN_USER:
            product = Product.objects.filter(id=product_id)
            if product.exists():
                product = product.first()
                product.status = 0
                product.save()
                return JsonResponse({'status': 'محصول با موفقیت حذف شد'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'حذف ناموفق'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'توکن صحیح نیست'}, status=status.HTTP_401_UNAUTHORIZED)

class AddCommentProduct(APIView):
    @staticmethod
    def post(request):
        data = request.data
        product_id = data.get('product_id')
        comment = data.get('comment') if 'comment' in data else None
        user_id = data.get('user_id')
        rate = data.get('rate')




        if token == TOKEN_USER:

            comment = ProductComment.objects.create(product_id=product_id, comment=comment, rate=rate,
                                                    user_id=user_id)
            if comment:
                return JsonResponse({'status':'نظر شما با موفقیت ثبت شد'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'ثبت نظر ناموفق'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'توکن صحیح نیست'}, status=status.HTTP_401_UNAUTHORIZED)