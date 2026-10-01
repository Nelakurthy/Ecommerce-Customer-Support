
from django.db import models
from django.contrib.auth.models import User


# ==========================================
# PRODUCT
# ==========================================

class Product(models.Model):

    name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.name


# ==========================================
# FAQ
# ==========================================

class FAQ(models.Model):

    question = models.CharField(
        max_length=255
    )

    answer = models.TextField()

    keywords = models.CharField(
        max_length=500,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.question


# ==========================================
# ORDER
# ==========================================

class Order(models.Model):

    STATUS_CHOICES = [

        ("Placed", "Placed"),

        ("Confirmed", "Confirmed"),

        ("Shipped", "Shipped"),

        ("Out for Delivery", "Out for Delivery"),

        ("Delivered", "Delivered"),

        ("Cancelled", "Cancelled"),

    ]


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    order_id = models.CharField(
        max_length=50,
        unique=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Placed"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return (
            f"{self.order_id} - "
            f"{self.status}"
        )


# ==========================================
# CONVERSATION
# ==========================================

class Conversation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.created_at}"
        )


# ==========================================
# SUPPORT TICKET
# ==========================================

class SupportTicket(models.Model):

    STATUS_CHOICES = [

        ("Open", "Open"),

        ("In Progress", "In Progress"),

        ("Resolved", "Resolved"),

    ]


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=255
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return (
            f"{self.subject} - "
            f"{self.status}"
        )
