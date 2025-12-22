from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


@register_snippet
class AircraftCategory(models.Model):
    """Aircraft category (Light Jet, Midsize, Heavy, etc.)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('order'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name = "Aircraft Category"
        verbose_name_plural = "Aircraft Categories"


@register_snippet
class Aircraft(ClusterableModel):
    """Aircraft model with specs - managed from admin"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        AircraftCategory,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='aircraft'
    )
    
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    interior_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    short_description = models.TextField(blank=True)
    full_description = RichTextField(blank=True)
    
    passengers = models.IntegerField(default=8, help_text="Maximum passengers")
    range_nm = models.IntegerField(default=3000, help_text="Range in nautical miles")
    speed_knots = models.IntegerField(default=450, help_text="Max speed in knots")
    baggage_capacity = models.CharField(max_length=100, blank=True, help_text="e.g. 120 cu ft")
    
    cabin_height = models.CharField(max_length=50, blank=True)
    cabin_width = models.CharField(max_length=50, blank=True)
    cabin_length = models.CharField(max_length=50, blank=True)
    
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        help_text="Starting hourly rate in USD"
    )
    
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('category'),
            FieldPanel('is_featured'),
            FieldPanel('is_available'),
            FieldPanel('order'),
        ], heading="Basic Info"),
        MultiFieldPanel([
            FieldPanel('main_image'),
            FieldPanel('interior_image'),
        ], heading="Images"),
        MultiFieldPanel([
            FieldPanel('short_description'),
            FieldPanel('full_description'),
        ], heading="Description"),
        MultiFieldPanel([
            FieldPanel('passengers'),
            FieldPanel('range_nm'),
            FieldPanel('speed_knots'),
            FieldPanel('baggage_capacity'),
        ], heading="Performance"),
        MultiFieldPanel([
            FieldPanel('cabin_height'),
            FieldPanel('cabin_width'),
            FieldPanel('cabin_length'),
        ], heading="Cabin Dimensions"),
        FieldPanel('hourly_rate'),
    ]
    
    def __str__(self):
        return self.name
    
    @property
    def range_display(self):
        return f"{self.range_nm:,} nm"
    
    @property
    def speed_display(self):
        return f"{self.speed_knots} kts"
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Aircraft"
        verbose_name_plural = "Aircraft"


class FleetPage(Page):
    """Fleet listing page"""
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    parent_page_types = ['home.HomePage']
    
    def get_context(self, request):
        context = super().get_context(request)
        context['categories'] = AircraftCategory.objects.all()
        context['aircraft'] = Aircraft.objects.filter(is_available=True)
        context['featured_aircraft'] = Aircraft.objects.filter(is_featured=True, is_available=True)
        return context
    
    class Meta:
        verbose_name = "Fleet Page"


class AircraftDetailPage(Page):
    """Individual aircraft detail page"""
    aircraft = models.ForeignKey(
        Aircraft,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='pages'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('aircraft'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        if self.aircraft:
            context['aircraft'] = self.aircraft
        return context
    
    class Meta:
        verbose_name = "Aircraft Detail Page"
