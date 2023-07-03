from django.db import models


# Create your models here.
class User(models.Model):
    FULL_NAME_MAX_LENGTH = 100
    USERNAME_MAX_LENGTH = 50
    EMAIL_MAX_LENGTH = 254
    COUNTRY_MAX_LENGTH = 50
    ADDRESS_MAX_LENGTH = 200

    full_name = models.CharField(max_length=FULL_NAME_MAX_LENGTH, default="Full name")
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)
    country = models.CharField(max_length=COUNTRY_MAX_LENGTH, default="Country")
    address = models.CharField(max_length=ADDRESS_MAX_LENGTH, default="Address")

    wallet_address = models.CharField(
        max_length=100
    )  # Assuming wallet address is a string

    def __str__(self):
        return self.username


class Item(models.Model):
    seller_wallet_address = models.CharField(max_length=100)
    id_item = models.IntegerField()
    name = models.CharField(max_length=100)
    imageLink = models.ImageField(upload_to="item_images")
    description = models.TextField()
    price = models.DecimalField(max_digits=50, decimal_places=2)
    quantity = models.PositiveIntegerField()
    postingFee = models.DecimalField(max_digits=50, decimal_places=2)

    @property
    def total_posting_fee(self):
        return self.posting_fee * self.quantity

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    seller_wallet_address = models.CharField(max_length=100)
    buyer_wallet_address = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    item_id = models.IntegerField()
    price = models.DecimalField(max_digits=50, decimal_places=2)
    quantity = models.PositiveIntegerField()
    rewards = models.DecimalField(max_digits=50, decimal_places=2)
    state = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Order #{self.id}"
