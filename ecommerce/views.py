from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import (
    Item,
    OrderItem,
    Order,
    Address,
)
from .serializers import (
    ItemSerializer,
    OrderItemSerializer,
    # OrderListSerializer,
    OrderSerializer,
    AddressSerializer,
    )
from .permissions import IsStaffOrReadOnly
from rest_framework.filters import SearchFilter


class ItemMVS(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsStaffOrReadOnly,]
    lookup_field = "slug"
    filter_backends = [SearchFilter]
    # filterset_fields=['title']
    search_fields=['description']


class OrderItemMVS(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return OrderItem.objects.all()
        
        return OrderItem.objects.filter(user=user, ordered=False)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        orderItem_queryset = OrderItem.objects.filter(user_id=request.user.id, item_id=request.data["item_id"], ordered=False)
        
        if orderItem_queryset.exists():
            data ={
                "message": "You already have this item"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            OrderItem.objects.create(user_id=request.user.id, item_id=request.data["item_id"], quantity=request.data["quantity"])
            data ={
                "message": "ADDED"
            }
            return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if 'quantity' in request.data and request.data['quantity'] == 0:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

# class OrderListView(ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderListSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_staff:
#             return Order.objects.all()
        
#         return Order.objects.filter(user=user)
    
# class OrderCreateView(CreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_staff:
#             return Order.objects.all()
        
#         return Order.objects.filter(user=user)

# class OrderDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_staff:
#             return Order.objects.all()
        
#         return Order.objects.filter(user=user)
    
class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        return Order.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        for i in request.data["items"]:
            orderItem = OrderItem.objects.get(id=i)
            orderItem.ordered = True
            orderItem.save()
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class AddressMVS(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Address.objects.all()
        
        return Address.objects.filter(user=user)
