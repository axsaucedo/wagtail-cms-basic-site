from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Airport(models.Model):
    """Airport/Location for flight booking"""
    code = models.CharField(max_length=10, unique=True, help_text="ICAO or IATA code")
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, help_text="e.g. North America, Europe")
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    timezone = models.CharField(max_length=50, blank=True)
    is_popular = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    panels = [
        MultiFieldPanel([
            FieldPanel('code'),
            FieldPanel('name'),
            FieldPanel('city'),
            FieldPanel('country'),
            FieldPanel('region'),
        ], heading="Location Info"),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),
            FieldPanel('timezone'),
        ], heading="Coordinates"),
        MultiFieldPanel([
            FieldPanel('is_popular'),
            FieldPanel('is_available'),
        ], heading="Settings"),
    ]
    
    def __str__(self):
        return f"{self.code} - {self.city}, {self.country}"
    
    @property
    def display_name(self):
        return f"{self.city} ({self.code})"
    
    class Meta:
        ordering = ['city']
        verbose_name = "Airport"
        verbose_name_plural = "Airports"


@register_snippet
class FlightRoute(models.Model):
    """Pre-defined flight routes with pricing"""
    origin = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='routes_from'
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='routes_to'
    )
    
    distance_nm = models.IntegerField(help_text="Distance in nautical miles")
    estimated_flight_time = models.CharField(max_length=50, help_text="e.g. 2h 30m")
    
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Base price in USD"
    )
    
    is_popular = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    panels = [
        MultiFieldPanel([
            FieldPanel('origin'),
            FieldPanel('destination'),
        ], heading="Route"),
        MultiFieldPanel([
            FieldPanel('distance_nm'),
            FieldPanel('estimated_flight_time'),
            FieldPanel('base_price'),
        ], heading="Details"),
        MultiFieldPanel([
            FieldPanel('is_popular'),
            FieldPanel('is_available'),
        ], heading="Settings"),
    ]
    
    def __str__(self):
        return f"{self.origin.code} → {self.destination.code}"
    
    class Meta:
        unique_together = ['origin', 'destination']
        verbose_name = "Flight Route"
        verbose_name_plural = "Flight Routes"


class FlightInquiry(models.Model):
    """Flight quote/inquiry submissions"""
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    passengers = models.IntegerField(default=1)
    
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    
    aircraft_preference = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('quoted', 'Quoted'),
            ('booked', 'Booked'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='new'
    )
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.departure_date})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Flight Inquiry"
        verbose_name_plural = "Flight Inquiries"
