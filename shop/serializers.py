from rest_framework import serializers

from .models import *


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ['fio', 'email', 'password']

    def save(self, **kwargs):
        user = UserCustom(
            fio=self.validated_data['fio'],
            email=self.validated_data['email'],
            username=self.validated_data['fio'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    color = ColorsSerializer()
    size = SizeSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price', 'image', 'is_new_collection', 'color', 'size']


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'order_price', 'delivery_method', 'delivery_address', 'comment', 'created_at']

    

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_price', 'delivery_method', 'delivery_address', 'comment']
