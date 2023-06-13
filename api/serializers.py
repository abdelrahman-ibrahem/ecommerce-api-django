from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Order, Product, ProductCart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = [
            'owner',
            'product',
            'quantity'
        ]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'name'
        ]


class CustomUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()


class MyCartSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = ProductCart
        fields = [
            'owner',
            'product',
            'quantity'
        ]


class OrderSerializers(serializers.ModelSerializer):

    owner = CustomUserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.Serializer):
    phone = serializers.CharField()
    address = serializers.CharField()
    email = serializers.EmailField(required=False)


class CreateUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    phone = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'name',
            'phone'
        ]


class CreateUserSerializerResponse(serializers.Serializer):
    token = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()
