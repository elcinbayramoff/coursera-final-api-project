from django.shortcuts import render, get_object_or_404
from rest_framework import generics,authentication, permissions,status
from .models import MenuItem,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,UserSerializer,CartSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User,Group
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from .permissions import IsAdminOrManager,IsNotInAnyGroup
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class MenuItemsView(generics.ListCreateAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'title']
    filterset_fields = ['price', 'title']
    search_fields = ['title','category__title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def perform_create(self, serializer):
        if not (self.request.user.groups.filter(name='manager').exists() or self.request.user.is_staff):
            raise PermissionDenied("Permission denied.")
        serializer.save()

class SingleMenuItemsView(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def has_permission(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_staff

    def perform_update(self, serializer):
        if not self.has_permission():
            raise PermissionDenied("Permission denied.")
        serializer.save()
    def perform_destroy(self, instance):
        if not self.has_permission():
            raise PermissionDenied("Permission denied.")
        instance.delete()
        
class GroupUserApiView(APIView):
    permission_classes = [IsAdminOrManager]

    def get(self, request, group_name):
        group = get_object_or_404(Group, name=group_name)
        users = group.user_set.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, group_name):
        group = get_object_or_404(Group, name=group_name)
        post_data = request.data
        username = post_data.get('username', '')

        # Retrieve the existing user by username or return a 404 response if not found
        user = User.objects.filter(username=username).first()

        if user is not None:
            if user not in group.user_set.all():
                group.user_set.add(user)
                serializer = UserSerializer(user)
                return Response({"message": "User added to the group", "user_data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "User is already in the group"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User with that username not found"}, status=status.HTTP_400_BAD_REQUEST)

class RemoveUserFromGroup(APIView):
    permission_classes = [IsAdminOrManager]

    def delete(self, request, group_name, user_id):
        group = get_object_or_404(Group, name=group_name)
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)

        if(group.user_set.filter(id=user_id)):
            group.user_set.remove(user)
            return Response({"message": "User removed from the group successfully!", "user_data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "User not found in the group", "user_data": serializer.data}, status=status.HTTP_404_NOT_FOUND)
    


# views.py

class CartView(generics.ListCreateAPIView,generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsNotInAnyGroup]

    def perform_create(self, serializer):
        user = self.request.user
        title = self.request.data.get('menuitem_title')
        quantity = self.request.data.get('quantity')

        try:
            # Attempt to get the existing cart item for the user and menu item
            cart_item = Cart.objects.get(user=user, menuitem__title=title)

            # If the cart item exists, increment the quantity
            cart_item.quantity += int(quantity)
            cart_item.price = cart_item.unit_price * cart_item.quantity
            cart_item.save()

            # No need to continue with the creation, as it's already updated
            return
        except Cart.DoesNotExist:
            pass  # Continue with creating a new cart item

        # If the cart item doesn't exist, create a new one
        menu_item = MenuItem.objects.get(title=title)
        serializer.save(user=user, menuitem=menu_item, quantity=quantity, unit_price=menu_item.price, price=menu_item.price * int(quantity))

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    def destroy(self, request, *args, **kwargs):
        # Get all cart items for the current user
        queryset = self.get_queryset()

        # Delete all cart items
        queryset.delete()

        return Response({"detail": "All cart items deleted successfully."}, status=204)
    
class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_price = sum(item.price for item in cart)
        
        # Create Order
        order_serializer = OrderSerializer(data={'user': user, 'total_price': total_price})
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save(user=user, total_price=total_price)

        # Create Order Items
        order_item_serializer = OrderItemSerializer()
        for cart_item in cart:
            menu_item = cart_item.menuitem
            order_item_data = {
                'order': order,
                'menuitem': menu_item,
                'quantity': cart_item.quantity,
                'unit_price': menu_item.price,
                'price': cart_item.price
            }
            order_item_serializer.create(order_item_data)
        cart.delete()
        return Response({"detail": "Order created successfully."})

    def get(self, request):
        if request.user.groups.count()==0:
            user = request.user
            orders = Order.objects.filter(user=user)
            order_serializer = OrderSerializer(orders, many=True)

            # Manually include related order items in the serialized data
            serialized_data = order_serializer.data

            return Response(serialized_data)
        elif request.user.groups.filter(name='manager').exists():
            orders = Order.objects.all()
            order_serializer = OrderSerializer(orders,many=True)
            serialized_data = order_serializer.data
            return Response(serialized_data)
        elif request.user.groups.filter(name='delivery_crew').exists():
            user_id = self.request.user.id
            orders = Order.objects.filter(delivery_crew=user_id)
            serialized_data = OrderSerializer(orders,many=True).data
            return Response(serialized_data)
    def delete(self,request):
        user = request.user
        orders = Order.objects.filter(user=user)
        orders.delete()
        return Response({"message":"Deleted succesfully"})

    
class SingleOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # You might adjust this based on your needs
    serializer_class = OrderSerializer

    def get_order(self, order_id):
        try:
            order = Order.objects.get(id=order_id)
            return order
        except Order.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        if(request.user.groups.count()==0):
            order_id = kwargs.get('pk')
            order = self.get_order(order_id)
            if not order:
                return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            if not order.user==request.user:
                return Response({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif(request.user.groups.filter(name='manager').exists()):
            order_id = kwargs.get('pk')
            order = self.get_order(order_id)
            if not order:
                return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif(request.user.groups.filter(name='delivery_crew').exists()):
            order_id = kwargs.get('pk')
            order = self.get_order(order_id)
            if not order:
                return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            if not order.delivery_crew==request.user:
                return Response({"detail": "No permission"}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(order)
            return Response(serializer.data, status=status.HTTP_200_OK)       
            
            
    def put(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        order = self.get_order(order_id)
        if not order:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.groups.filter(name='manager').exists() or request.user.groups.count() == 0:
            serializer = self.serializer_class(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        order = self.get_order(order_id)
        if not order:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if(request.user.groups.filter(name='manager').exists()):
            serializer = self.serializer_class(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif(request.user.groups.filter(name='delivery_crew').exists()):
            if 'status' in request.data and len(request.data.keys()) == 1 and order.delivery_crew == request.user:
                serializer = self.serializer_class(order, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        elif(request.user.groups.count()==0):
            if 'orderitem' in request.data and len(request.data.keys()) == 1:
                serializer = self.serializer_class(order, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "You don't have permission to perform PATCH method"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        if(request.user.groups.filter(name='manager').exists()==0):
            return Response({"error":"You don't have permissions to perform Delete method"})
        order_id = kwargs.get('pk')
        order = self.get_order(order_id)
        if not order:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"detail": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)