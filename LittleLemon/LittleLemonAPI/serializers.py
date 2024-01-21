from rest_framework import serializers
from .models import Cart,Category,MenuItem,Order,OrderItem
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
from django.utils import timezone
class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']
        extra_kwargs = {
            'price':{'min_value':0}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username'] 


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_title = serializers.CharField(write_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price','menuitem_title']
        read_only_fields = ['user', 'menuitem', 'unit_price', 'price']
    def create(self, validated_data):
        menuitem_title = validated_data.pop('menuitem_title', None)
        menu_item = MenuItem.objects.get(title=menuitem_title)

        validated_data['menuitem'] = menu_item
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()
    class Meta:
        model = OrderItem
        fields = ['order','menuitem','quantity','unit_price','price']
        read_only_fields = ['order','menuitem','quantity','unit_price','price']
        
class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=6,decimal_places=2,write_only=True)
    orderitem = OrderItemSerializer(read_only=True,many=True, source='orderitem_set')
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','status','total','date','total_price','orderitem']
        read_only_fields = ['id','user','total','date','orderitem']
    def create(self, validated_data):
        total_price = validated_data.pop('total_price', None)
        validated_data['total']=total_price
        validated_data['date'] = timezone.now().date()  

        return super().create(validated_data)