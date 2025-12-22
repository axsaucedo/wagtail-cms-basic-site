"""
Management command to set up initial Wagtail site with sample content.
"""
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import HomePage, ExperiencePage, ContactPage, SiteSettings, MenuItem
from fleet.models import Aircraft, AircraftCategory, FleetPage
from booking.models import Airport


class Command(BaseCommand):
    help = 'Set up initial Wagtail site with sample content'
    
    def handle(self, *args, **options):
        self.stdout.write('Setting up FlyMex site...')
        
        # Get the root page
        root = Page.objects.filter(depth=1).first()
        if not root:
            self.stdout.write(self.style.ERROR('No root page found. Run: python manage.py migrate'))
            return
        
        # Create or get HomePage
        home_page = HomePage.objects.first()
        
        if not home_page:
            # Check if there's a default welcome page at depth 2
            existing_home = Page.objects.filter(depth=2).first()
            
            if existing_home:
                # Delete the existing default page
                existing_home.delete()
            
            # Create new HomePage as child of root using treebeard directly
            home_page = HomePage(
                title='FlyMex Aero',
                slug='home',
                seo_title='FlyMex - Flying Private Made Simple | Luxury Jet Charter',
                body=[],
                depth=2,
                path='00010001',
            )
            home_page.save()
            home_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created HomePage'))
        else:
            self.stdout.write('HomePage already exists')
        
        # Update or create Site to point to our homepage
        site = Site.objects.first()
        if site:
            site.root_page = home_page
            site.site_name = 'FlyMex Aero'
            site.is_default_site = True
            site.save()
            self.stdout.write(self.style.SUCCESS('Updated Site configuration'))
        else:
            Site.objects.create(
                hostname='*',
                port=80,
                site_name='FlyMex Aero',
                root_page=home_page,
                is_default_site=True,
            )
            self.stdout.write(self.style.SUCCESS('Created Site configuration'))
        
        # Create Fleet Page as child of HomePage
        fleet_page = FleetPage.objects.first()
        if not fleet_page:
            fleet_page = FleetPage(
                title='Our Fleet',
                slug='fleet',
                intro='<p>Discover our world-class fleet of private jets, from light jets for short trips to heavy jets for transcontinental travel.</p>',
                depth=3,
                path='000100010001',
            )
            fleet_page.save()
            fleet_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created Fleet Page'))
        else:
            self.stdout.write('Fleet Page already exists')
        
        # Create Experience Page as child of HomePage
        experience_page = ExperiencePage.objects.first()
        if not experience_page:
            experience_page = ExperiencePage(
                title='The Experience',
                slug='experience',
                intro='<p>Experience the pinnacle of private aviation with FlyMex. Every journey is crafted with precision and care.</p>',
                body=[],
                depth=3,
                path='000100010002',
            )
            experience_page.save()
            experience_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created Experience Page'))
        else:
            self.stdout.write('Experience Page already exists')
        
        # Create Contact Page as child of HomePage
        contact_page = ContactPage.objects.first()
        if not contact_page:
            contact_page = ContactPage(
                title='Contact',
                slug='contact',
                intro='<p>Get in touch with our team to plan your next private flight.</p>',
                phone='+52 55 4601 1670',
                email='info@flymex.aero',
                address='Toluca International Airport\nHangar Zone\nToluca, Mexico',
                body=[],
                depth=3,
                path='000100010003',
            )
            contact_page.save()
            contact_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS('Created Contact Page'))
        else:
            self.stdout.write('Contact Page already exists')
        
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
            ('Light Jets', 'Perfect for short trips with up to 7 passengers.', 1),
            ('Midsize Jets', 'Ideal balance of comfort and range for 8-9 passengers.', 2),
            ('Super Midsize Jets', 'Enhanced cabin space and transcontinental range.', 3),
            ('Heavy Jets', 'Maximum luxury and range for 10-16 passengers.', 4),
        ]
        
        for name, desc, order in categories_data:
            cat, created = AircraftCategory.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'order': order}
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
        
        # Clear old menu items and create new ones linked to pages
        MenuItem.objects.all().delete()
        
        menu_items = [
            {'title': 'Fleet', 'page': fleet_page, 'order': 1},
            {'title': 'Experience', 'page': experience_page, 'order': 2},
            {'title': 'Contact', 'page': contact_page, 'order': 3},
        ]
        
        for data in menu_items:
            MenuItem.objects.create(**data)
            self.stdout.write(f'Created menu item: {data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('Site setup complete!'))
        self.stdout.write('')
        self.stdout.write('Pages created:')
        self.stdout.write(f'  - Home: /')
        self.stdout.write(f'  - Fleet: /fleet/')
        self.stdout.write(f'  - Experience: /experience/')
        self.stdout.write(f'  - Contact: /contact/')
        self.stdout.write('')
        self.stdout.write('To customize content:')
        self.stdout.write('1. Go to /admin/')
        self.stdout.write('2. Login with your superuser credentials')
        self.stdout.write('3. Click on Pages to edit any page')
