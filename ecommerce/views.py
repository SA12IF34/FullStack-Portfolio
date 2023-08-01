from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTStatelessUserAuthentication, JWTTokenUserAuthentication
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import stripe
 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

stripe.api_key = 'sk_test_51LpvauANvpfKL0QVNt3Cz5Ba8zra1P9PAfrjGUoNWEYQZIu8Td8rQ7yT2krXjWvCV9Nuh03LsrSQ4DJtfHT4KHgH00bI89VkGP'

DOMAIN = 'http://localhost:5173/buy/'

class CheckoutAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request):

        return Response(status=HTTP_200_OK)
    
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NV79zANvpfKL0QVllZRZbzQ',
                        'quantity': 1,
                        
                    },
                ],
                mode='payment',
                success_url=DOMAIN + '?success=true',
                cancel_url=DOMAIN + '?canceled=true',
            )
        except Exception as e:
            print(e.args)
            return Response(exception=e)
        print(checkout_session.url)
        return Response(data={'url':checkout_session.url})


class UserAPI(APIView):

    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTStatelessUserAuthentication]

    def post(self, request):

        print(request.COOKIES)

        if not User.objects.filter(username=request.data['username'], email=request.data['email']).exists():
            user = User.objects.create_user(first_name=request.data['first_name'], last_name=request.data['last_name'], username=request.data['username'], email=request.data['email'], password=request.data['password'])

            serializer = UserSerializer(instance=user)
            
            return Response(data=serializer.data, status=HTTP_201_CREATED)
    
        return Response(status=HTTP_306_RESERVED) # user already exists, sign in if the account is yours

# class LoginAPI(APIView):

#     permission_classes = [permissions.AllowAny]


#     def post(self, request):


#         serializer = LoginSerializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.validate(attrs=request.data)

#             res = Response(status=HTTP_202_ACCEPTED)

#             return res

#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) # Check from data or sign up
    
# class LogoutAPI(APIView):

#     def get(self, request):
#         return Response(status=HTTP_200_OK)
    
#     def post(self, request):
#         print(request.COOKIES)
#         logout(request)

#         return Response(status=HTTP_202_ACCEPTED)


class CartsAPI(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request):
        
        user = request.user 
        perfumes = Cart.objects.filter(user=user.id)
        serializer = CartSerializer(instance=perfumes, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        
        user = request.user.id
        request.data['user'] = user
        serializer = CartSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)


class CartAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request, name):
        user = request.user.id
        perfume = Cart.objects.get(perfume_name=name, user=user)
        serializer = CartSerializer(instance=perfume)

        return Response(data=serializer.data, status=HTTP_200_OK)
    
    def delete(self, request, name):
        user = request.user.id
        perfume = Cart.objects.get(perfume_name=name, user=user)
        perfume.delete()

        return Response(status=HTTP_202_ACCEPTED)
    


class BoughtsAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request):
        user = request.user.id    
        
        perfumes = Buy.objects.filter(user=user)
        serializer = BuySerializer(instance=perfumes, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        user = request.user.id
        request.data['user'] = user
        serializer = BuySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(data=serializer.data, status=HTTP_201_CREATED)
    
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)


class BoughtAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request, name):
        user = request.user.id

        perfume = Buy.objects.get(perfume_name=name, user=user)
        serializer = BuySerializer(instance=perfume)

        return Response(data=serializer.data, status=HTTP_200_OK)
     
