from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.snippets.models import register_snippet


class HeroBlock(blocks.StructBlock):
    """Hero section with background image and CTA"""
    background_image = ImageChooserBlock(required=True)
    headline = blocks.CharBlock(max_length=200, help_text="Main headline")
    subheadline = blocks.CharBlock(max_length=300, required=False)
    cta_text = blocks.CharBlock(max_length=50, default="Book Your Flight")
    show_flight_picker = blocks.BooleanBlock(required=False, default=True)
    
    class Meta:
        template = 'blocks/hero_block.html'
        icon = 'image'
        label = 'Hero Section'


class MembershipCardBlock(blocks.StructBlock):
    """Membership tier card"""
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    link_text = blocks.CharBlock(max_length=50, default="View membership")
    link_url = blocks.URLBlock(required=False)
    
    class Meta:
        template = 'blocks/membership_card_block.html'
        icon = 'user'
        label = 'Membership Card'


class MembershipsBlock(blocks.StructBlock):
    """Memberships section"""
    section_title = blocks.CharBlock(max_length=200, default="Memberships")
    section_description = blocks.TextBlock(required=False)
    cards = blocks.ListBlock(MembershipCardBlock())
    
    class Meta:
        template = 'blocks/memberships_block.html'
        icon = 'group'
        label = 'Memberships Section'


class ServiceBlock(blocks.StructBlock):
    """Individual service item"""
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    image = ImageChooserBlock(required=True)
    
    class Meta:
        template = 'blocks/service_block.html'
        icon = 'cog'
        label = 'Service'


class ServicesBlock(blocks.StructBlock):
    """Services section with numbered items"""
    section_subtitle = blocks.CharBlock(max_length=100, default="SERVICES")
    section_title = blocks.CharBlock(max_length=200, default="Our solutions are different")
    section_description = blocks.TextBlock(required=False)
    services = blocks.ListBlock(ServiceBlock())
    
    class Meta:
        template = 'blocks/services_block.html'
        icon = 'list-ul'
        label = 'Services Section'


class ImageTextBlock(blocks.StructBlock):
    """Image with text content - alternating layout"""
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(max_length=200)
    content = blocks.RichTextBlock()
    link_text = blocks.CharBlock(max_length=50, required=False)
    link_url = blocks.URLBlock(required=False)
    image_position = blocks.ChoiceBlock(choices=[
        ('left', 'Image Left'),
        ('right', 'Image Right'),
    ], default='left')
    
    class Meta:
        template = 'blocks/image_text_block.html'
        icon = 'image'
        label = 'Image & Text'


class TestimonialBlock(blocks.StructBlock):
    """Testimonial/quote"""
    quote = blocks.TextBlock()
    author = blocks.CharBlock(max_length=100)
    title = blocks.CharBlock(max_length=100, required=False)
    image = ImageChooserBlock(required=False)
    
    class Meta:
        template = 'blocks/testimonial_block.html'
        icon = 'openquote'
        label = 'Testimonial'


class CertificationBlock(blocks.StructBlock):
    """Safety certification logo"""
    name = blocks.CharBlock(max_length=100)
    logo = ImageChooserBlock(required=True)
    
    class Meta:
        icon = 'doc-full'
        label = 'Certification'


class SafetyCertificationsBlock(blocks.StructBlock):
    """Safety and certifications section"""
    section_subtitle = blocks.CharBlock(max_length=100, default="SAFETY AND CERTIFICATION")
    section_title = blocks.CharBlock(max_length=200, default="Commitment to safety")
    section_description = blocks.TextBlock(required=False)
    certifications = blocks.ListBlock(CertificationBlock())
    
    class Meta:
        template = 'blocks/safety_certifications_block.html'
        icon = 'success'
        label = 'Safety & Certifications'


class CTABlock(blocks.StructBlock):
    """Call to action section"""
    background_image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=200)
    button_text = blocks.CharBlock(max_length=50, default="Book Your Flight")
    
    class Meta:
        template = 'blocks/cta_block.html'
        icon = 'pick'
        label = 'Call to Action'


class FleetHighlightBlock(blocks.StructBlock):
    """Fleet highlight section"""
    section_subtitle = blocks.CharBlock(max_length=100, default="DISCOVER OUR FLEET")
    section_title = blocks.CharBlock(max_length=200)
    section_description = blocks.TextBlock(required=False)
    
    class Meta:
        template = 'blocks/fleet_highlight_block.html'
        icon = 'view'
        label = 'Fleet Highlight'


class ExperienceBlock(blocks.StructBlock):
    """Experience section"""
    section_subtitle = blocks.CharBlock(max_length=100, default="THE BEST EXPERIENCE")
    title = blocks.CharBlock(max_length=200)
    description = blocks.TextBlock()
    image = ImageChooserBlock(required=True)
    link_text = blocks.CharBlock(max_length=50, required=False)
    link_url = blocks.URLBlock(required=False)
    
    class Meta:
        template = 'blocks/experience_block.html'
        icon = 'snippet'
        label = 'Experience Section'


class HomePage(Page):
    """Homepage with StreamField content"""
    
    body = StreamField([
        ('hero', HeroBlock()),
        ('fleet_highlight', FleetHighlightBlock()),
        ('memberships', MembershipsBlock()),
        ('services', ServicesBlock()),
        ('image_text', ImageTextBlock()),
        ('experience', ExperienceBlock()),
        ('safety_certifications', SafetyCertificationsBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    # Allow these page types as children
    subpage_types = ['home.ExperiencePage', 'home.ContactPage', 'home.GenericPage', 'fleet.FleetPage']
    
    class Meta:
        verbose_name = "Home Page"


class ExperiencePage(Page):
    """Experience/About page with StreamField content"""
    
    intro = RichTextField(blank=True)
    
    body = StreamField([
        ('image_text', ImageTextBlock()),
        ('services', ServicesBlock()),
        ('experience', ExperienceBlock()),
        ('safety_certifications', SafetyCertificationsBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    parent_page_types = ['home.HomePage']
    
    class Meta:
        verbose_name = "Experience Page"


class ContactPage(Page):
    """Contact page"""
    
    intro = RichTextField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    
    body = StreamField([
        ('image_text', ImageTextBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Contact Details"),
        FieldPanel('body'),
    ]
    
    parent_page_types = ['home.HomePage']
    
    class Meta:
        verbose_name = "Contact Page"


class GenericPage(Page):
    """Generic content page for any purpose"""
    
    body = StreamField([
        ('hero', HeroBlock()),
        ('image_text', ImageTextBlock()),
        ('services', ServicesBlock()),
        ('experience', ExperienceBlock()),
        ('safety_certifications', SafetyCertificationsBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    parent_page_types = ['home.HomePage']
    
    class Meta:
        verbose_name = "Generic Page"


@register_snippet
class SiteSettings(models.Model):
    """Global site settings manageable from admin"""
    site_name = models.CharField(max_length=100, default="FlyMex Aero")
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    phone_number = models.CharField(max_length=50, default="+52 55 4601 1670")
    email = models.EmailField(default="info@flymex.aero")
    
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    footer_text = models.TextField(blank=True, default="FlyMex - Flying private made simple")
    
    panels = [
        MultiFieldPanel([
            FieldPanel('site_name'),
            FieldPanel('logo'),
            FieldPanel('phone_number'),
            FieldPanel('email'),
        ], heading="Site Info"),
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('twitter_url'),
            FieldPanel('instagram_url'),
            FieldPanel('linkedin_url'),
        ], heading="Social Media"),
        FieldPanel('footer_text'),
    ]
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


@register_snippet
class MenuItem(models.Model):
    """Navigation menu item"""
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500, blank=True)
    page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    order = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    
    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
        FieldPanel('page'),
        FieldPanel('order'),
        FieldPanel('parent'),
    ]
    
    def __str__(self):
        return self.title
    
    @property
    def link(self):
        if self.page:
            return self.page.url
        return self.url or '#'
    
    class Meta:
        ordering = ['order']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
