import json
import re
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from .models import Airport, FlightRoute, FlightInquiry


def airports_api(request):
    """API endpoint for airport autocomplete"""
    query = request.GET.get('q', '').strip()
    
    airports = Airport.objects.filter(is_available=True)
    
    if query:
        airports = airports.filter(
            Q(code__icontains=query) |
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query)
        )
    else:
        airports = airports.filter(is_popular=True)
    
    airports = airports[:20]
    
    data = [
        {
            'code': a.code,
            'name': a.name,
            'city': a.city,
            'country': a.country,
            'display': a.display_name,
        }
        for a in airports
    ]
    
    return JsonResponse({'airports': data})


@require_http_methods(["POST"])
def flight_quote_api(request):
    """API endpoint for flight quote requests with validation"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['origin', 'destination', 'departure_date', 'name', 'email']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return JsonResponse({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing)}',
            }, status=400)
        
        # Validate email format
        email = data.get('email', '')
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.',
            }, status=400)
        
        # Validate passengers
        try:
            passengers = int(data.get('passengers', 1))
            if passengers < 1 or passengers > 50:
                raise ValueError()
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'message': 'Passengers must be a number between 1 and 50.',
            }, status=400)
        
        inquiry = FlightInquiry.objects.create(
            origin=data.get('origin', ''),
            destination=data.get('destination', ''),
            departure_date=data.get('departure_date'),
            return_date=data.get('return_date') or None,
            passengers=passengers,
            name=data.get('name', ''),
            email=email,
            phone=data.get('phone', ''),
            message=data.get('message', ''),
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Your flight inquiry has been received. Our team will contact you shortly.',
            'inquiry_id': inquiry.id,
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format.',
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.',
        }, status=500)


@ensure_csrf_cookie
def get_csrf_token(request):
    """Endpoint to get CSRF token for form submissions"""
    return JsonResponse({'success': True})
