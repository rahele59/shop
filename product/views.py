from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render

from product.models import ProductImage, Product
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
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED)
