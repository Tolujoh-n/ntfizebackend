from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Item, Order
from .serializers import UserSerializer, ItemSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import sys

sys.path.append("..")
from events import fetch_event


class MyView(APIView):
    def get(self, request):
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)


class ItemListAPIView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serialized_items = []
        for item in items:
            # print(item.imageLink.url)
            serialized_item = {
                "id": item.id,
                "seller_wallet_address": item.seller_wallet_address,
                "id_item": item.id_item,
                "name": item.name,
                "imageLink": item.imageLink.url,  # Get the full image URL
                "description": item.description,
                "price": item.price,
                "quantity": item.quantity,
                "postingFee": item.postingFee,
            }
            serialized_items.append(serialized_item)
        return Response(serialized_items)


from django.shortcuts import get_object_or_404


class ProductDetailAPIView(APIView):
    def get(self, request, id_item):
        product = get_object_or_404(Item, id_item=id_item)
        serialized_product = {
            "id": product.id,
            "seller_wallet_address": product.seller_wallet_address,
            "id_item": product.id_item,
            "name": product.name,
            "imageLink": product.imageLink.url,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "postingFee": product.postingFee,
        }
        return Response(serialized_product)


class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"})
        return Response(serializer.errors, status=400)


from rest_framework.parsers import MultiPartParser, FormParser


class CreateItemAPIView(APIView):
    # This allows the view to handle file uploads
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Fetch the event details using the provided parameters
        contract_name = request.data.get("contract_name")
        chain_id = request.data.get("chain_id")
        transaction_hash = request.data.get("transaction_hash")
        event_name = request.data.get("event_name")

        # Call fetch_event function
        print(contract_name, chain_id, transaction_hash, event_name)
        data = fetch_event(contract_name, chain_id, transaction_hash, "ItemListed")

        print(data)
        print("***")
        print(request.data.get("postingFee"), request.FILES.get("image"))
        if data:
            # Create the Item object based on the fetched event data
            item_data = {
                "seller_wallet_address": data["seller"],
                "id_item": data[
                    "itemId"
                ],  # Assuming your Item model has a field called 'itemId'
                "name": data["name"],
                "imageLink": request.FILES.get(
                    "image"
                ),  # Getting the uploaded image file
                "description": data["description"],
                "price": data["price"],
                "quantity": data["quantity"],
                "postingFee": request.data.get("postingFee"),
                # ... Include other fields as necessary
            }

            print(item_data)

            # Use the serializer to validate and save the item data
            item_serializer = ItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item_serializer.save()
                return Response({"message": "Item created successfully"})
            else:
                # Handle serializer errors
                print(item_serializer.errors)
                return Response(item_serializer.errors, status=400)
        else:
            return Response({"message": "Failed to fetch event data"}, status=400)


class CreateOrderAPIView(APIView):
    def post(self, request):
        contract_name = request.data.get("contract_name")
        chain_id = request.data.get("chain_id")
        transaction_hash = request.data.get("transaction_hash")
        event_name = request.data.get("event_name")
        # item_id = request.data.get("item_id")

        # Fetch the event details and other necessary data using the provided parameters
        # ...
        data = fetch_event(contract_name, chain_id, transaction_hash, event_name)
        # if data:
        #     # Lookup the item based on the given item_id
        #     try:
        #         item = Item.objects.get(id=data["itemId"])
        #     except Item.DoesNotExist:
        #         # Handle case where item with the given item_id does not exist
        #         return Response({"message": "Item Not Found"})

        # Create the Order object based on the fetched event data and item connection
        order_data = {
            "seller_wallet_address": data["seller"],
            "buyer_wallet_address": data["buyer"],
            "order_id": str(data["order"]),  # User data from the fetched event
            "item_id": data["itemId"],  # Connect the item object to the order
            "price": data["price"],
            "quantity": data["quantity"],  # Quantity from the fetched event
            "rewards": data["rewards"],
            "state": "paid",  # Provide the initial status
        }
        print(order_data)
        print(event_name)

        order_serializer = OrderSerializer(data=order_data)

        if order_serializer.is_valid():
            order_serializer.save()
            return Response({"message": "Order created successfully"})
        else:
            # Handle serializer errors
            print(order_serializer.errors)
            return Response(order_serializer.errors, status=400)
        # else:
        #     return Response({"message": "Failed to fetch event data"}, status=400)


class UserOrdersAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serialized_orders = []
        for order in orders:
            try:
                item = Item.objects.get(id_item=order.item_id)
                serialized_order = {
                    "order_id": order.order_id,
                    "img": item.imageLink.url,
                    "name": item.name,
                    "price": order.price,
                    "quantity": order.quantity,
                    "rewards": order.rewards,
                    "status": order.state,
                }
                serialized_orders.append(serialized_order)
            except Item.DoesNotExist:
                # Handle the case where the item does not exist
                continue
        return Response(serialized_orders)


class UpdateOrderAPIView(APIView):
    def put(self, request, order_id):
        state = request.data.get(
            "state"
        )  # Get the desired new state from the request data

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": f"Order with ID {order_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        order.state = state
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class CancelOrderAPIView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.cancellation_requested = True
        instance.status = "cancelled"
        instance.save()
        return self.partial_update(request, *args, **kwargs)
