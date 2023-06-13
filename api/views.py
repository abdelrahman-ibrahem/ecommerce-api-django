
import traceback

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes as permission
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Order, Product, ProductCart, Profile
from .serializers import (AddToCartSerializer, CreateOrderSerializer,
                          CreateUserSerializer, CreateUserSerializerResponse,
                          MyCartSerializer, OrderSerializers,
                          ProductSerializer)


# for paginate data and return data per 1000
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

# Create new account using username, email, password and name


@swagger_auto_schema(methods=['POST'], request_body=CreateUserSerializer,
                     responses={200: CreateUserSerializerResponse})
@api_view(['POST'])
def register(request):
    try:
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        phone = data.get('phone')
        if username and email and password and name:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            profile = Profile(user=user, name=name, phone=phone)
            profile.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': "invalid data"
            })
    except Exception:
        print(traceback.format_exc())
        return Response(status=status.HTTP_409_CONFLICT)


# Display all products and create new product


class ListCreateProduct(generics.ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = ['name']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination

# Add product to cart, This functions get the product id, user, quantity of the product


@swagger_auto_schema(methods=['POST'], request_body=AddToCartSerializer)
@api_view(['POST'])
@permission([
    permissions.IsAuthenticated
])
def add_to_cart(request):
    try:
        product_id = request.data['product_id']
        quantity = request.data['quantity']
        user = request.user
        product = Product.objects.get(id=product_id)
        ProductCart.objects.create(
            owner=user, product=product, quantity=int(quantity))
        return Response({
            'message': "product is added to you cart"
        }, status=status.HTTP_201_CREATED)
    except Exception:
        print(traceback.format_exc())
        return Response(status=status.HTTP_409_CONFLICT)


# Display all products in use cart
class MyCart(generics.ListAPIView):
    queryset = ProductCart.objects.all()
    serializer_class = MyCartSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        qs = ProductCart.objects.filter(owner=self.request.user, ordered=False)
        return qs


'''
    Create new order
    
        - this functions get the phone, email and address 
            - and will create your order if you have a products in your cart
        - get all un ordered products on you cart and create new order 
'''


@swagger_auto_schema(methods=['POST'], request_body=CreateOrderSerializer)
@permission([
    permissions.IsAuthenticated
])
@api_view(['POST'])
def create_order(request):
    try:
        user = request.user
        data = request.data
        cart_item = ProductCart.objects.filter(
            owner=user,
            ordered=False
        )
        if cart_item.count() > 0:
            for product_item in cart_item:
                order = Order.objects.create(
                    owner=user,
                    product=product_item.product,
                    phone=data['phone'],
                    email=data['email'] or user.email,
                    address=data['address'],
                    quantity=product_item.quantity
                )
                order.save()
                product_item.ordered = True
                product_item.save()

                return Response({
                    'message': "Order Created"
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': "You dont have any product in your cart"
            })
    except Exception:
        print(traceback.format_exc())
        return Response(status=status.HTTP_409_CONFLICT)

# Get my all orders


class ListOrder(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    pagination_class = LargeResultsSetPagination
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.filter(owner=user)
        return qs
