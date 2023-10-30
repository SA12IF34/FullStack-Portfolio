from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.status import *
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTStatelessUserAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import stripe
from .models import *
from .serializers import *
import environ
import json
import os


env = environ.Env()
environ.Env.read_env()
# Token Authentication Configuration
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def authenticateJWT(user):  # creating authentication credentials
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignUpAPI(APIView):

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]


    def post(self, request):

        if not User.objects.filter(email=request.data['email']).exists():
            try:
                user = User.objects.create_user(first_name=request.data['first_name'], last_name=request.data['last_name'], username=request.data['username'], email=request.data['email'], password=request.data['password'])

                auth_creds = authenticateJWT(user)

                return Response(data=auth_creds, status=HTTP_201_CREATED)
            except:
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        else :

            return Response(data={'message': 'email is already used'}, status=HTTP_306_RESERVED) 


current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, 'data', 'perfume_data.json')
json_data = open(data_path, 'r', encoding='utf-8') 
perfumes_data = json.load(json_data)

class PerfumeAPI(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        perfume_name = request.data['perfume']
        perfume = filter(lambda p: p['name'] == perfume_name, perfumes_data['data'])

        return Response(data=list(perfume)[0], status=HTTP_200_OK)

class SearchAPI(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        
        return Response(data=perfumes_data, status=HTTP_200_OK)

    def post(self, request):
        
        data = []

        for key, value in request.data['filters'].items():
            filtered_data = []
            if key == 'name' and len(value) > 0:
                filtered_data = filter(lambda data: value in data[key].lower(), perfumes_data['data'])
            elif (key == 'for_gender' or key == 'company') and value != 'company' and value != 'gender':
                filtered_data = filter(lambda data: data[key] == value, perfumes_data['data'])
            elif key == 'main accords' and value != 'accords':
                filtered_data = filter(lambda data: value in data[key], perfumes_data['data'])
            elif 'notes' in key and value != 'notes':
                filtered_data = filter(lambda data: value in data[key], perfumes_data['data'])
            
            set_of_jsons = {json.dumps(d, sort_keys=True) for d in filtered_data}
            data.extend([json.loads(t) for t in set_of_jsons])
             
       
        return Response(data={'data': data}, status=HTTP_200_OK)


class CartAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request):
        user = request.user

        cart_objects = Cart.objects.filter(account=user.id)
        serializer = CartSerializer(instance=cart_objects, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        try:
            user = request.user

            serializer = CartSerializer(data={
                'product_name': request.data['product_name'],
                'price': request.data['price'],
                'image': request.data['image'],
                'account': user.id
            })

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(data=serializer.data, status=HTTP_201_CREATED)
        except:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, name):
        user = request.user
        cart_object = Cart.objects.get(product_name=name, account=user.id)
        cart_object.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class BoughtsAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        bought_objects = Bought.objects.filter(account=user.id)
        serializer = BoughtSerializer(instance=bought_objects, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)

    def post(self, request):
        # try:
        user = request.user
        serializer = BoughtSerializer(data={
            'product_name': request.data['product_name'],
            'image': request.data['image'],
            'account': user.id
        })

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(status=HTTP_201_CREATED)
        
        # except:
        #     return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)



stripe.api_key = env('STRIPE_API')

class CheckoutAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        return Response(status=HTTP_200_OK)

    def post(self, request):
        try:
            redirect_url = request.data['redirect']
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NV79zANvpfKL0QVllZRZbzQ',
                        'quantity': 1,
                        
                    },
                ],
                mode='payment',
                success_url=redirect_url + '?success=true',
                cancel_url=redirect_url + '?canceled=true',
            )
        except Exception as e:
            return Response(exception=e)
        return Response(data={'url':checkout_session.url}, status=HTTP_200_OK)

