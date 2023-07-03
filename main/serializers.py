from rest_framework import serializers
from .models import User, Item, Order


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "username",
            "country",
            "address",
            "wallet_address",
        ]

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
