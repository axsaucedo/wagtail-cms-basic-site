"""
Management command to set up initial Wagtail site with sample content.
"""
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import HomePage, SiteSettings, MenuItem
from fleet.models import Aircraft, AircraftCategory
from booking.models import Airport


class Command(BaseCommand):
    help = 'Set up initial Wagtail site with sample content'
    
    def handle(self, *args, **options):
        self.stdout.write('Setting up FlyMex site...')
        
        # Get the root page
        root = Page.objects.get(slug='root')
        
        # Create HomePage if not exists
        try:
            home_page = HomePage.objects.get()
            self.stdout.write('HomePage already exists')
        except HomePage.DoesNotExist:
            # Check if there's a default welcome page to replace
            existing_home = Page.objects.filter(depth=2).first()
            
            if existing_home and not isinstance(existing_home.specific, HomePage):
                # Replace the existing page
                home_page = HomePage(
                    title='FlyMex Aero',
                    slug='home',
                    seo_title='FlyMex - Flying Private Made Simple | Luxury Jet Charter',
                    body=[],
                    path=existing_home.path,
                    depth=existing_home.depth,
                )
                existing_home.delete()
                home_page.save()
                home_page.save_revision().publish()
                self.stdout.write(self.style.SUCCESS('Replaced default page with HomePage'))
            else:
                # Add new child
                home_page = HomePage(
                    title='FlyMex Aero',
                    slug='home',
                    seo_title='FlyMex - Flying Private Made Simple | Luxury Jet Charter',
                    body=[],
                )
                root.add_child(instance=home_page)
                home_page.save_revision().publish()
                self.stdout.write(self.style.SUCCESS('Created HomePage'))
        
        # Update Site to point to our homepage
        site = Site.objects.first()
        if site:
            site.root_page = home_page
            site.site_name = 'FlyMex Aero'
            site.save()
            self.stdout.write(self.style.SUCCESS('Updated Site configuration'))
        
        # Create site settings
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name='FlyMex Aero',
                phone_number='+52 55 4601 1670',
                email='info@flymex.aero',
                footer_text='FlyMex - Flying private made simple. 24 years of experience.'
            )
            self.stdout.write(self.style.SUCCESS('Created SiteSettings'))
        
        # Create aircraft categories
        categories_data = [
            ('Light Jets', 'Perfect for short trips with up to 7 passengers.'),
            ('Midsize Jets', 'Ideal balance of comfort and range for 8-9 passengers.'),
            ('Super Midsize Jets', 'Enhanced cabin space and transcontinental range.'),
            ('Heavy Jets', 'Maximum luxury and range for 10-16 passengers.'),
        ]
        
        for name, desc in categories_data:
            cat, created = AircraftCategory.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            if created:
                self.stdout.write(f'Created category: {name}')
        
        # Create sample aircraft
        aircraft_data = [
            {
                'name': 'Phenom 300',
                'category': 'Light Jets',
                'passengers': 7,
                'range_nm': 2010,
                'speed_knots': 453,
                'short_description': 'The best-selling light jet, combining performance, comfort, and efficiency.',
                'is_featured': True,
            },
            {
                'name': 'Citation CJ3+',
                'category': 'Light Jets',
                'passengers': 7,
                'range_nm': 2040,
                'speed_knots': 416,
                'short_description': 'Reliable performer with excellent cabin comfort and coast-to-coast range.',
            },
            {
                'name': 'Hawker 900XP',
                'category': 'Midsize Jets',
                'passengers': 8,
                'range_nm': 2930,
                'speed_knots': 466,
                'short_description': 'Spacious stand-up cabin with transatlantic capability.',
                'is_featured': True,
            },
            {
                'name': 'Learjet 60XR',
                'category': 'Midsize Jets',
                'passengers': 7,
                'range_nm': 2405,
                'speed_knots': 513,
                'short_description': 'Iconic performance with unmatched speed and climb capabilities.',
            },
            {
                'name': 'Challenger 350',
                'category': 'Super Midsize Jets',
                'passengers': 9,
                'range_nm': 3200,
                'speed_knots': 470,
                'short_description': 'Wide-body comfort with impressive range and performance.',
                'is_featured': True,
            },
            {
                'name': 'Gulfstream G280',
                'category': 'Super Midsize Jets',
                'passengers': 10,
                'range_nm': 3600,
                'speed_knots': 482,
                'short_description': 'Class-leading range and cabin comfort.',
            },
            {
                'name': 'Falcon 900LX',
                'category': 'Heavy Jets',
                'passengers': 12,
                'range_nm': 4750,
                'speed_knots': 481,
                'short_description': 'Tri-jet reliability with exceptional range and performance.',
                'is_featured': True,
            },
            {
                'name': 'Gulfstream G450',
                'category': 'Heavy Jets',
                'passengers': 14,
                'range_nm': 4350,
                'speed_knots': 528,
                'short_description': 'Ultimate in long-range luxury travel.',
            },
        ]
        
        for data in aircraft_data:
            cat_name = data.pop('category')
            category = AircraftCategory.objects.get(name=cat_name)
            aircraft, created = Aircraft.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'category': category}
            )
            if created:
                self.stdout.write(f'Created aircraft: {data["name"]}')
        
        # Create popular airports
        airports_data = [
            {'code': 'TLC', 'name': 'Toluca International Airport', 'city': 'Toluca', 'country': 'Mexico', 'region': 'Mexico', 'is_popular': True},
            {'code': 'MEX', 'name': 'Benito Juarez International', 'city': 'Mexico City', 'country': 'Mexico', 'region': 'Mexico', 'is_popular': True},
            {'code': 'CUN', 'name': 'Cancun International Airport', 'city': 'Cancun', 'country': 'Mexico', 'region': 'Mexico', 'is_popular': True},
            {'code': 'GDL', 'name': 'Miguel Hidalgo y Costilla', 'city': 'Guadalajara', 'country': 'Mexico', 'region': 'Mexico', 'is_popular': True},
            {'code': 'MTY', 'name': 'Mariano Escobedo International', 'city': 'Monterrey', 'country': 'Mexico', 'region': 'Mexico', 'is_popular': True},
            {'code': 'SJD', 'name': 'Los Cabos International', 'city': 'San Jose del Cabo', 'country': 'Mexico', 'region': 'Mexico', 'is_popular': True},
            {'code': 'PVR', 'name': 'Gustavo Diaz Ordaz', 'city': 'Puerto Vallarta', 'country': 'Mexico', 'region': 'Mexico', 'is_popular': True},
            {'code': 'MIA', 'name': 'Miami International Airport', 'city': 'Miami', 'country': 'USA', 'region': 'North America', 'is_popular': True},
            {'code': 'LAX', 'name': 'Los Angeles International', 'city': 'Los Angeles', 'country': 'USA', 'region': 'North America', 'is_popular': True},
            {'code': 'JFK', 'name': 'John F Kennedy International', 'city': 'New York', 'country': 'USA', 'region': 'North America', 'is_popular': True},
            {'code': 'LAS', 'name': 'Harry Reid International', 'city': 'Las Vegas', 'country': 'USA', 'region': 'North America', 'is_popular': True},
            {'code': 'HOU', 'name': 'William P Hobby Airport', 'city': 'Houston', 'country': 'USA', 'region': 'North America', 'is_popular': True},
        ]
        
        for data in airports_data:
            airport, created = Airport.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created airport: {data["code"]} - {data["city"]}')
        
        # Create menu items
        menu_items_data = [
            {'title': 'Fleet', 'url': '/fleet/', 'order': 1},
            {'title': 'Experience', 'url': '/experience/', 'order': 2},
            {'title': 'Safety', 'url': '/safety/', 'order': 3},
            {'title': 'Contact', 'url': '/contact/', 'order': 4},
        ]
        
        for data in menu_items_data:
            item, created = MenuItem.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created menu item: {data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('Site setup complete!'))
        self.stdout.write('')
        self.stdout.write('To add content to the homepage:')
        self.stdout.write('1. Go to /admin/')
        self.stdout.write('2. Login with your superuser credentials')
        self.stdout.write('3. Click on Pages > Home')
        self.stdout.write('4. Add StreamField blocks (Hero, Fleet Highlight, etc.)')
        self.stdout.write('5. Upload images in Images section')
