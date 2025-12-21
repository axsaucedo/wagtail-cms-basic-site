# FlyMex Aero - Luxury Private Jet Charter Website

## Overview
A luxury private jet charter website inspired by VistaJet, built with Django Wagtail CMS. This project enables non-technical users to manage all website content including pages, aircraft fleet, flight locations, and booking inquiries.

## Tech Stack
- **Backend**: Django 6.0 + Wagtail 6.4 CMS
- **Frontend**: Django Templates + Tailwind CSS (via CDN)
- **Database**: SQLite (development) / PostgreSQL ready
- **Server**: Django development server on port 5000

## Project Structure
```
/
├── flymex_site/        # Django project settings
│   ├── settings.py     # Main configuration
│   ├── urls.py         # URL routing
│   └── wsgi.py         # WSGI entry point
├── home/               # Homepage app with StreamField blocks
│   ├── models.py       # HomePage, SiteSettings, MenuItem
│   └── management/     # setup_site command
├── fleet/              # Aircraft fleet app
│   └── models.py       # Aircraft, AircraftCategory, FleetPage
├── booking/            # Flight booking app
│   ├── models.py       # Airport, FlightRoute, FlightInquiry
│   └── views.py        # API endpoints for quotes
├── templates/          # Django templates
│   ├── base.html       # Base template with Tailwind
│   ├── partials/       # Header, footer, modal components
│   ├── blocks/         # StreamField block templates
│   └── home/           # Homepage template
├── static/             # Static assets
│   ├── css/main.css    # Custom styles
│   ├── js/main.js      # JavaScript interactions
│   └── images/         # Logo SVGs
└── requirements.txt    # Python dependencies
```

## Admin Access
- **URL**: `/admin/`
- **Username**: `admin`
- **Password**: `admin123`

## CMS Features

### Pages (Wagtail Admin)
- **HomePage**: Uses StreamField with these block types:
  - Hero Section (with background image and CTA)
  - Fleet Highlight
  - Memberships Section
  - Services Section (accordion style)
  - Image & Text blocks
  - Experience Section
  - Safety & Certifications
  - Call to Action

### Snippets (Wagtail Admin > Snippets)
- **Aircraft**: Manage jet fleet with specs (passengers, range, speed)
- **Aircraft Categories**: Light Jets, Midsize, Super Midsize, Heavy
- **Airports**: Global airport database for booking
- **Flight Routes**: Pre-defined routes with pricing
- **Site Settings**: Contact info, social links, footer text
- **Menu Items**: Navigation structure

### Flight Inquiries
View and manage customer flight quote requests at Django Admin > Flight Inquiries

## API Endpoints
- `GET /api/airports/?q=search` - Airport autocomplete
- `POST /api/flight-quote/` - Submit flight inquiry

## Running the Project
The workflow runs: `python manage.py runserver 0.0.0.0:5000`

## Adding Content
1. Go to `/admin/` and login
2. Navigate to Pages > Home
3. Click Edit and add StreamField blocks
4. Upload images in Images section first
5. Save and Publish changes

## Development Notes
- Uses Tailwind CSS via CDN (replace with build process for production)
- Static files collected to `/staticfiles/`
- Media files stored in `/media/`
- SQLite database at `db.sqlite3`

## Recent Changes
- December 2024: Initial Django Wagtail setup
- Created HomePage with StreamField blocks
- Built fleet, booking apps with Wagtail snippets
- Implemented flight booking modal with autocomplete
- Added sample data: 8 aircraft, 12 airports, 4 categories
