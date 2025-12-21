from django.contrib import admin
from .models import FlightInquiry


@admin.register(FlightInquiry)
class FlightInquiryAdmin(admin.ModelAdmin):
    list_display = ['origin', 'destination', 'departure_date', 'passengers', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['origin', 'destination', 'name', 'email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
