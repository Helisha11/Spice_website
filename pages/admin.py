from django.contrib import admin
from .models import Product, FAQ, VisitorRegistration, ContactMessage

from .models import Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "position")
    list_editable = ("is_active", "position")
    search_fields = ("question", "answer")

@admin.register(VisitorRegistration)
class VisitorRegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "phone")
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Customer Information", {
            "fields": ("name", "email", "phone")
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "message_preview")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at", "name", "email", "message")
    fieldsets = (
        ("Customer Information", {
            "fields": ("name", "email")
        }),
        ("Message", {
            "fields": ("message",)
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
    
    def message_preview(self, obj):
        """Display a preview of the message in list view"""
        preview = obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
        return preview
    message_preview.short_description = "Message"
    
    def has_add_permission(self, request):
        """Prevent admin from manually adding contact messages"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion for cleaning up old messages"""
        return True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "phone")
    readonly_fields = ("created_at",)
    inlines = []


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    search_fields = ("order__name", "product__name")
