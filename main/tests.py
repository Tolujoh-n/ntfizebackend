# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from unittest.mock import patch
# from .models import User, Item, Order
# from .serializers import UserSerializer, ItemSerializer, OrderSerializer


# class CreateItemAPITestCase(APITestCase):
#     @patch("./views.fetch_event")
#     def test_create_item(self, mock_fetch_event):
#         # Mock the response of fetch_event
#         mock_fetch_event.return_value = {
#             "seller": "0xfD7059Cf48Ef2417a1b6Eeac9A77b6CA2D94A34e",
#             "id_item": 0,
#             "name": "Item1",
#             "image": "IMG.png",
#             "description": "Description",
#             "price": 10000000000000000000,
#             "quantity": 2,
#             "postingFee": 20000000000000000000,
#         }
#         # Define the endpoint url
#         url = reverse("create_item")  # Replace with the name of your endpoint

#         # Define the data that would be sent in the POST request
#         data = {
#             "contract_name": "some_contract_name",
#             "chain_id": "some_chain_id",
#             "transaction_hash": "some_transaction_hash",
#             "event_name": "some_event_name",
#             "item_id": "some_item_id",
#         }

#         # Simulate the POST request
#         response = self.client.post(url, data, format="json")

#         # Check if the response has a 201 status code, meaning the item was created
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Check if an item was added to the database
#         self.assertEqual(Item.objects.count(), 1)

#         # Check if the item in the database matches what was posted
#         item = Item.objects.get()
#         serializer = ItemSerializer(item)
#         self.assertEqual(serializer.data, response.data)
