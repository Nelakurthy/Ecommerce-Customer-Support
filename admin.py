from django.contrib import admin

from .models import (
    Product,
    FAQ,
    Order,
    Conversation,
    SupportTicket
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "created_at",
    )

    search_fields = (
        "name",
        "category",
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "created_at",
    )

    search_fields = (
        "question",
        "keywords",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_id",
        "user",
        "product",
        "quantity",
        "total_amount",
        "status",
        "created_at",
    )

    search_fields = (
        "order_id",
        "user__username",
    )

    list_filter = (
        "status",
        "created_at",
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "message",
        "response",
        "created_at",
    )

    search_fields = (
        "user__username",
        "message",
    )


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "subject",
        "status",
        "created_at",
    )

    search_fields = (
        "user__username",
        "subject",
    )

    list_filter = (
        "status",
        "created_at",
    )