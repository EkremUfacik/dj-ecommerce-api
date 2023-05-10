from rest_framework import serializers

from .models import (
    Item,
    OrderItem,
    Order,
    Address,
)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "id",
            "title",
            "price",
            "category",
            "image",
            "description",
            "slug",
        )


class OrderItemSerializer(serializers.ModelSerializer):

    item = ItemSerializer(read_only=True)
    item_id = serializers.IntegerField()
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only=True)
    item_total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "user",
            "user_id",
            "ordered",
            "item",
            "item_id",
            "quantity",
            "item_total_price"
        )

    def get_item_total_price(self, obj):
        return obj.quantity * obj.item.price
    
    # def create(self, validated_data):
    #     validated_data["user_id"] = self.context["request"].user.id
    #     instance = OrderItem.objects.create(**validated_data)
    #     return instance

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id", 
            "user",
            "address",
            "city",
            "country",
        )

# class OrderListSerializer(serializers.ModelSerializer):

#     items = OrderItemSerializer(many=True, required=True)
#     order_total_price = serializers.SerializerMethodField()
#     address = AddressSerializer(read_only=True)
#     address_id = serializers.IntegerField()

#     class Meta:
#         model = Order
#         fields = (
#             "id",
#             "user",
#             "items",
#             "start_date",
#             "shipping_date",
#             "ordered",
#             "address_id",
#             "address", 
#             "payment",
#             "order_total_price"
#         )
    
#     def get_order_total_price(self, obj):
#         items = obj.items.all()

#         total = 0

#         for i in items:
#             total += i.quantity * i.item.price
#         return total

# class OrderSerializer(serializers.ModelSerializer):

#     order_total_price = serializers.SerializerMethodField()
#     address = AddressSerializer(read_only=True)
#     address_id = serializers.IntegerField()
#     user = serializers.StringRelatedField()
#     user_id = serializers.IntegerField()
#     class Meta:
#         model = Order
#         fields = (
#             "id",
#             "user_id",
#             "user",
#             "items",
#             "start_date",
#             "shipping_date",
#             "ordered",
#             "address_id",
#             "address",  
#             "payment",
#             "order_total_price"
#         )
    
#     def get_order_total_price(self, obj):
#         items = obj.items.all()

#         total = 0

#         for i in items:
#             total += i.quantity * i.item.price
#         return total
    
class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True, read_only=True)
    order_total_price = serializers.SerializerMethodField()
    address = AddressSerializer(read_only=True)
    address_id = serializers.IntegerField()
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Order
        fields = (
            "id",
            "user_id",
            "user",
            "items",
            "start_date",
            "shipping_date",
            "ordered",
            "address_id",
            "address",  
            "payment",
            "order_total_price"
        )
    
    def get_order_total_price(self, obj):
        items = obj.items.all()

        total = 0

        for i in items:
            total += i.quantity * i.item.price
        return total
    
    # def create(self, validated_data):
    #     # print(validated_data, "eeeeeeeeeeee")
    #     # items_data = validated_data.pop("items_data") 
    #     order = Order.objects.create(user=self.context['request'].user)
    #     order.items.set(validated_data["items"])
    #     order.save()
    #     return order
    
    def create(self, validated_data):
        items = self.context['request'].data.get('items', [])
        order = Order.objects.create(user=self.context['request'].user)
        order.items.set(items)
        order.save()

        return order