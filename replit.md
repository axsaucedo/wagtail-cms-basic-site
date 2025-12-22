# FlyMex Aero - Luxury Private Jet Charter Website

## Overview
A luxury private jet charter website inspired by VistaJet, built with Django Wagtail CMS. This project enables non-technical users to manage all website content including pages, aircraft fleet, flight locations, and booking inquiries through a user-friendly admin panel.

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
│   ├── models.py       # HomePage, ExperiencePage, ContactPage, GenericPage
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
│   ├── home/           # HomePage, ExperiencePage, ContactPage templates
│   └── fleet/          # FleetPage template
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

## Live Pages
- **/** - Home page with hero section and flight booking
- **/fleet/** - Aircraft fleet listing with categories
- **/experience/** - The FlyMex experience page
- **/contact/** - Contact information and quote form

## CMS Features

### Pages (Wagtail Admin > Pages)
All pages are editable through the Wagtail admin. Each page type has StreamField for flexible content:

- **HomePage**: Hero, Fleet Highlight, Memberships, Services, Experience, Safety, CTA blocks
- **FleetPage**: Displays aircraft from database, editable intro text
- **ExperiencePage**: Image/Text, Services, Experience, Safety, CTA blocks
- **ContactPage**: Contact details (phone, email, address) plus StreamField content
- **GenericPage**: For any other content needs

### Snippets (Wagtail Admin > Snippets)
- **Aircraft**: Manage jet fleet with specs (passengers, range, speed, images)
- **Aircraft Categories**: Light Jets, Midsize, Super Midsize, Heavy
- **Airports**: Global airport database for booking autocomplete
- **Flight Routes**: Pre-defined routes with pricing
- **Site Settings**: Contact info, social links, footer text
- **Menu Items**: Navigation structure linked to pages

### Flight Inquiries
View and manage customer flight quote requests at `/admin/` under the Booking section

## API Endpoints
- `GET /api/airports/?q=search` - Airport autocomplete
- `POST /api/flight-quote/` - Submit flight inquiry (CSRF protected)
- `GET /api/csrf-token/` - Get CSRF token for forms

## Running the Project
The workflow runs: `python manage.py runserver 0.0.0.0:5000`

## Editing Content
1. Go to `/admin/` and login (admin / admin123)
2. Click **Pages** in the sidebar
3. Click on any page to edit its content
4. Use StreamField blocks to add/arrange content
5. Click **Publish** to make changes live

## Adding Aircraft
1. Go to `/admin/` > **Snippets** > **Aircraft**
2. Click **Add Aircraft**
3. Fill in name, category, specs, and upload images
4. Save - it will automatically appear on the Fleet page

## Development Notes
- Uses Tailwind CSS via CDN (replace with build process for production)
- Static files served from `/static/`
- Media files stored in `/media/`
- SQLite database at `db.sqlite3`

## Security Features
- CSRF protection on all form submissions
- Input validation on flight quote API
- Secure session handling

## Recent Changes
- December 2024: Initial Django Wagtail setup
- Created HomePage with StreamField blocks
- Built fleet, booking apps with Wagtail snippets
- Implemented flight booking modal with autocomplete
- Added ExperiencePage, ContactPage, GenericPage models
- Fixed page routing so all pages are editable via CMS
- Added sample data: 8 aircraft, 12 airports, 4 categories
