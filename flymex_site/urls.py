from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.models import Site, Page

from booking import views as booking_views


def health_check(request):
    """Health check endpoint that validates the site is properly configured."""
    errors = []
    
    try:
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            errors.append("No default site configured")
        elif not site.root_page:
            errors.append("Site has no root page")
    except Exception as e:
        errors.append(f"Database error: {str(e)}")
    
    try:
        page_count = Page.objects.filter(live=True).count()
        if page_count < 2:
            errors.append(f"Only {page_count} live pages found (expected at least 4)")
    except Exception as e:
        errors.append(f"Page query error: {str(e)}")
    
    if errors:
        return JsonResponse({
            "status": "error",
            "errors": errors
        }, status=500)
    
    return JsonResponse({
        "status": "ok",
        "site": site.site_name if site else None,
        "live_pages": page_count
    })


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    path('api/airports/', booking_views.airports_api, name='airports_api'),
    path('api/flight-quote/', booking_views.flight_quote_api, name='flight_quote_api'),
    path('api/csrf-token/', booking_views.get_csrf_token, name='csrf_token'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

urlpatterns += [
    re_path(r'', include(wagtail_urls)),
]
