from django.contrib import admin
from .models import Painting, Order

@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ("title", "artist_name", "year_created", "is_available")
    search_fields = ("title", "artist_name")
    list_filter = ("is_available",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_phone", "created_at")
    search_fields = ("customer_name", "customer_phone")
    list_filter = ("created_at",)
