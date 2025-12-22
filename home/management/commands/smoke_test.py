"""
Smoke test command to validate site configuration before deployment.
Run: python manage.py smoke_test
"""
from django.core.management.base import BaseCommand
from django.test import Client
from wagtail.models import Site, Page
from home.models import HomePage
from fleet.models import FleetPage, Aircraft, AircraftCategory
from booking.models import Airport


class Command(BaseCommand):
    help = 'Run smoke tests to validate site is ready for deployment'
    
    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('FlyMex Smoke Test')
        self.stdout.write('=' * 60)
        
        errors = []
        
        self.stdout.write('\n1. Checking database configuration...')
        
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            errors.append("No default site configured")
        elif not site.root_page:
            errors.append("Site has no root page")
        else:
            self.stdout.write(f'   Site: {site.site_name}')
        
        if not HomePage.objects.filter(live=True).exists():
            errors.append("No live HomePage found")
        
        if not FleetPage.objects.filter(live=True).exists():
            errors.append("No live FleetPage found")
        
        cat_count = AircraftCategory.objects.count()
        if cat_count == 0:
            errors.append("No aircraft categories found")
        else:
            self.stdout.write(f'   Aircraft categories: {cat_count}')
        
        aircraft_count = Aircraft.objects.count()
        if aircraft_count == 0:
            errors.append("No aircraft found")
        else:
            self.stdout.write(f'   Aircraft: {aircraft_count}')
        
        airport_count = Airport.objects.count()
        if airport_count == 0:
            errors.append("No airports found")
        else:
            self.stdout.write(f'   Airports: {airport_count}')
        
        page_tree_ok = True
        root = Page.objects.filter(depth=1).first()
        if root and root.numchild == 0:
            page_tree_ok = False
            errors.append("Root page numchild is 0 - page tree is broken")
        
        home = HomePage.objects.first()
        if home and home.numchild == 0:
            child_count = Page.objects.filter(depth=3, path__startswith=home.path).count()
            if child_count > 0:
                page_tree_ok = False
                errors.append(f"HomePage numchild is 0 but has {child_count} children - page tree is broken")
        
        self.stdout.write('\n2. Checking page responses...')
        client = Client()
        
        pages_to_check = [
            ('/', 'Home'),
            ('/fleet/', 'Fleet'),
            ('/experience/', 'Experience'),
            ('/contact/', 'Contact'),
            ('/health/', 'Health Check'),
        ]
        
        for url, name in pages_to_check:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    self.stdout.write(f'   {name} ({url}): OK')
                else:
                    errors.append(f"{name} page ({url}) returned status {response.status_code}")
                    self.stdout.write(self.style.ERROR(f'   {name} ({url}): FAILED ({response.status_code})'))
            except Exception as e:
                errors.append(f"{name} page ({url}) error: {str(e)}")
                self.stdout.write(self.style.ERROR(f'   {name} ({url}): ERROR'))
        
        self.stdout.write('\n' + '=' * 60)
        if errors:
            self.stdout.write(self.style.ERROR(f'SMOKE TEST FAILED - {len(errors)} error(s)'))
            self.stdout.write('=' * 60)
            for err in errors:
                self.stdout.write(self.style.ERROR(f'  - {err}'))
            self.stdout.write('\nTo fix, run: python manage.py setup_site')
            raise SystemExit(1)
        else:
            self.stdout.write(self.style.SUCCESS('SMOKE TEST PASSED - Site is ready for deployment'))
            self.stdout.write('=' * 60)
