from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import *
from .serializers import *


@permission_classes([AllowAny])
@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'data': {
                'user_token': token.key
            }}, status=201)
        else:
            return Response({'error': {
                'code': 422,
                'message': 'Validation error',
                'errors': serializer.errors
            }}, status=422)


@permission_classes([AllowAny])
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if not user:
                return Response({'error': {
                    'code': 401,
                    'message': 'Authentication failed'
                }}, status=401)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'data': {
                'user_token': token.key
            }}, status=201)
        else:
            return Response({'error': {'code': 422, 'message': 'Validation error', 'errors': serializer.errors}},
                            status=422)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def logout(request):
    if not request.user.is_authenticated:
        return Response({'error': {'code': 403, 'message': 'Login failed'}}, status=403)
    request.user.auth_token.delete()
    return Response({'data': {
        'message': 'logout'
    }}, status=200)


@permission_classes([AllowAny])
@api_view(['GET'])
def products(request):
    category_id = request.GET.get('category_id')
    if category_id is not None:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({'data': serializer.data}, status=200)

@permission_classes([AllowAny])
@api_view(['GET'])
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response({'data': serializer.data}, status=200)


@permission_classes([IsAdminUser])
@api_view(['POST'])
def product_add(request):
    if not request.user.is_authenticated:
        return Response({'error': {'code': 403, 'message': 'Login failed'}}, status=403)
    if not request.user.is_staff:
        return Response({'error': {'code': 403, 'message': 'Forbidden for you'}}, status=403)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data': {
            'id': serializer.data['id'],
            'message': 'Product added'
        }}, status=201)
    else:
        return Response({'error': {'code': 422, 'message': 'Validation error', 'errors': serializer.errors}},
                        status=422)


@permission_classes([IsAdminUser])
@api_view(['GET', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    if not request.user.is_authenticated:
        return Response({'error': {'code': 403, 'message': 'Login failed'}}, status=403)
    if not request.user.is_staff:
        return Response({'error': {'code': 403, 'message': 'Forbidden for you'}}, status=403)
    try:
        prod = Product.objects.get(pk=pk)
    except:
        return Response({'error': {'code': 404, 'message': 'Not found'}}, status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(prod)
        return Response({'data': serializer.data}, status=200)
    if request.method == 'PATCH':
        serializer = ProductSerializer(data=request.data, instance=prod, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=200)
        else:
            return Response({'error': {'code': 422, 'message': 'Validation error', 'errors': serializer.errors}},
                            status=422)
    if request.method == 'DELETE':
        prod.delete()
        return Response({"data": {"message": "Product removed"}}, status=200)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def cart_view(request):
    if not request.user.is_authenticated:
        return Response({'error': {'code': 403, 'message': 'Login failed'}}, status=403)
    if request.user.is_staff:
        return Response({'error': {'code': 403, 'message': 'Forbidden for you'}}, status=403)

    if request.method == 'GET':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response({'data': serializer.data['products']}, status=200)


@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def cart_update(request, pk):
    if not request.user.is_authenticated:
        return Response({'error': {'code': 403, 'message': 'Login failed'}}, status=403)
    if request.user.is_staff:
        return Response({'error': {'code': 403, 'message': 'Forbidden for you'}}, status=403)
    try:
        prod = Product.objects.get(pk=pk)
    except:
        return Response({'error': {'code': 404, 'message': 'Not found'}}, status=404)

    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(prod)
        return Response({'data': {'message': 'Product add to card'}}, status=201)

    if request.method == 'DELETE':
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(prod)
        return Response({'data': {'message': 'item removed from cart'}}, status=200)


@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def get_create_order(request):
    if not request.user.is_authenticated:
        return Response({'error': {'code': 403, 'message': 'Login failed'}}, status=403)
    if request.user.is_staff:
        return Response({'error': {'code': 403, 'message': 'Forbidden for you'}}, status=403)

    if request.method == "GET":
        order = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(order, many=True)
        return Response({'data': serializer.data}, status=200)

    if request.method == 'POST':
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            return Response({'error': {'code': 422, 'message': 'Cart is empty'}}, status=422)
        order = Order.objects.create(user=request.user)
        for product in cart.products.all():
            order.products.add(product)
            order.order_price += product.price
        
        order.delivery_address = serializer.validated_data['delivery_address']
        order.delivery_method = serializer.validated_data['delivery_method']
        order.comment = serializer.validated_data['comment']
        order.save()
        cart.delete()
        serializer = OrderSerializer(order)
        return Response({'data': {'order_id': serializer.data['id'], 'message': 'Order is processed'}}, status=201)
