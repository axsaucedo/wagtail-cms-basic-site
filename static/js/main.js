/**
 * FlyMex Aero - Main JavaScript
 * Smooth interactions and animations for the luxury jet charter website
 */

document.addEventListener('DOMContentLoaded', function() {
    initHeader();
    initMobileMenu();
    initFlightModal();
    initScrollAnimations();
    initServiceAccordion();
    initAirportAutocomplete();
    initFlightForm();
});

/**
 * Header scroll behavior
 */
function initHeader() {
    const header = document.getElementById('main-header');
    if (!header) return;
    
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
}

/**
 * Mobile menu toggle
 */
function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    const overlay = document.getElementById('mobile-menu-overlay');
    const closeBtn = document.getElementById('mobile-menu-close');
    
    if (!btn || !menu) return;
    
    btn.addEventListener('click', function() {
        menu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    function closeMenu() {
        menu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    if (closeBtn) closeBtn.addEventListener('click', closeMenu);
    if (overlay) overlay.addEventListener('click', closeMenu);
}

/**
 * Flight booking modal
 */
function initFlightModal() {
    const modal = document.getElementById('flight-modal');
    const bookBtn = document.getElementById('book-flight-btn');
    
    if (!modal) return;
    
    if (bookBtn) {
        bookBtn.addEventListener('click', openFlightModal);
    }
    
    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeFlightModal();
        }
    });
}

function openFlightModal() {
    const modal = document.getElementById('flight-modal');
    if (!modal) return;
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Focus first input
    setTimeout(function() {
        const firstInput = modal.querySelector('input[type="text"]');
        if (firstInput) firstInput.focus();
    }, 300);
}

function closeFlightModal() {
    const modal = document.getElementById('flight-modal');
    if (!modal) return;
    
    modal.classList.remove('active');
    document.body.style.overflow = '';
    
    // Reset form
    const form = document.getElementById('flight-quote-form');
    const success = document.getElementById('form-success');
    if (form) form.classList.remove('hidden');
    if (success) success.classList.add('hidden');
}

// Make functions globally accessible
window.openFlightModal = openFlightModal;
window.closeFlightModal = closeFlightModal;

/**
 * Scroll animations
 */
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    if (!elements.length) return;
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    elements.forEach(function(el) {
        observer.observe(el);
    });
}

/**
 * Service accordion
 */
function initServiceAccordion() {
    const headers = document.querySelectorAll('.service-header');
    
    headers.forEach(function(header) {
        header.addEventListener('click', function() {
            const accordion = this.closest('.service-accordion');
            const isActive = accordion.classList.contains('active');
            
            // Close all accordions
            document.querySelectorAll('.service-accordion').forEach(function(acc) {
                acc.classList.remove('active');
            });
            
            // Open clicked one if it wasn't active
            if (!isActive) {
                accordion.classList.add('active');
            }
        });
    });
    
    // Open first accordion by default
    const firstAccordion = document.querySelector('.service-accordion');
    if (firstAccordion) {
        firstAccordion.classList.add('active');
    }
}

/**
 * Airport autocomplete
 */
function initAirportAutocomplete() {
    const originInput = document.getElementById('origin-input');
    const destInput = document.getElementById('destination-input');
    const originSuggestions = document.getElementById('origin-suggestions');
    const destSuggestions = document.getElementById('destination-suggestions');
    
    if (originInput && originSuggestions) {
        setupAutocomplete(originInput, originSuggestions);
    }
    
    if (destInput && destSuggestions) {
        setupAutocomplete(destInput, destSuggestions);
    }
}

function setupAutocomplete(input, suggestionsEl) {
    let debounceTimer;
    
    input.addEventListener('input', function() {
        const query = this.value.trim();
        
        clearTimeout(debounceTimer);
        
        if (query.length < 2) {
            suggestionsEl.classList.add('hidden');
            return;
        }
        
        debounceTimer = setTimeout(function() {
            fetchAirports(query, suggestionsEl, input);
        }, 300);
    });
    
    input.addEventListener('focus', function() {
        const query = this.value.trim();
        if (query.length >= 2) {
            fetchAirports(query, suggestionsEl, input);
        }
    });
    
    input.addEventListener('blur', function() {
        // Delay to allow click on suggestion
        setTimeout(function() {
            suggestionsEl.classList.add('hidden');
        }, 200);
    });
}

function fetchAirports(query, suggestionsEl, input) {
    fetch('/api/airports/?q=' + encodeURIComponent(query))
        .then(function(response) { return response.json(); })
        .then(function(data) {
            renderSuggestions(data.airports, suggestionsEl, input);
        })
        .catch(function(error) {
            console.error('Error fetching airports:', error);
            // Show some default suggestions for demo
            renderSuggestions(getDefaultAirports(query), suggestionsEl, input);
        });
}

function getDefaultAirports(query) {
    const airports = [
        { code: 'TLC', name: 'Toluca Intl Airport', city: 'Toluca', country: 'Mexico' },
        { code: 'MEX', name: 'Benito Juarez Intl', city: 'Mexico City', country: 'Mexico' },
        { code: 'CUN', name: 'Cancun Intl', city: 'Cancun', country: 'Mexico' },
        { code: 'GDL', name: 'Miguel Hidalgo y Costilla', city: 'Guadalajara', country: 'Mexico' },
        { code: 'MTY', name: 'Mariano Escobedo Intl', city: 'Monterrey', country: 'Mexico' },
        { code: 'SJD', name: 'Los Cabos Intl', city: 'San Jose del Cabo', country: 'Mexico' },
        { code: 'MIA', name: 'Miami Intl', city: 'Miami', country: 'USA' },
        { code: 'LAX', name: 'Los Angeles Intl', city: 'Los Angeles', country: 'USA' },
        { code: 'JFK', name: 'John F Kennedy Intl', city: 'New York', country: 'USA' },
        { code: 'LAS', name: 'Harry Reid Intl', city: 'Las Vegas', country: 'USA' },
    ];
    
    const q = query.toLowerCase();
    return airports.filter(function(a) {
        return a.code.toLowerCase().includes(q) ||
               a.city.toLowerCase().includes(q) ||
               a.name.toLowerCase().includes(q) ||
               a.country.toLowerCase().includes(q);
    }).slice(0, 5);
}

function renderSuggestions(airports, suggestionsEl, input) {
    if (!airports || !airports.length) {
        suggestionsEl.classList.add('hidden');
        return;
    }
    
    suggestionsEl.innerHTML = airports.map(function(airport) {
        return '<div class="suggestion-item" data-code="' + airport.code + '" data-display="' + airport.city + ' (' + airport.code + ')">' +
               '<span class="code">' + airport.code + '</span> - ' + airport.city + ', ' + airport.country +
               '</div>';
    }).join('');
    
    suggestionsEl.classList.remove('hidden');
    
    // Add click handlers
    suggestionsEl.querySelectorAll('.suggestion-item').forEach(function(item) {
        item.addEventListener('click', function() {
            input.value = this.dataset.display;
            suggestionsEl.classList.add('hidden');
        });
    });
}

/**
 * Passenger counter
 */
function updatePassengers(delta) {
    const countEl = document.getElementById('passenger-count');
    const inputEl = document.getElementById('passengers-input');
    
    if (!countEl || !inputEl) return;
    
    let count = parseInt(inputEl.value) || 1;
    count = Math.max(1, Math.min(20, count + delta));
    
    countEl.textContent = count;
    inputEl.value = count;
}

window.updatePassengers = updatePassengers;

/**
 * Get CSRF token from cookie
 */
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Flight quote form submission
 */
function initFlightForm() {
    const form = document.getElementById('flight-quote-form');
    
    if (!form) return;
    
    // Ensure CSRF cookie is set
    fetch('/api/csrf-token/', { credentials: 'same-origin' });
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = {};
        
        formData.forEach(function(value, key) {
            data[key] = value;
        });
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        const csrfToken = getCsrfToken();
        
        fetch('/api/flight-quote/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'same-origin',
            body: JSON.stringify(data)
        })
        .then(function(response) { return response.json(); })
        .then(function(result) {
            if (result.success) {
                form.classList.add('hidden');
                document.getElementById('form-success').classList.remove('hidden');
            } else {
                alert(result.message || 'Something went wrong. Please try again.');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            // For demo, show success anyway
            form.classList.add('hidden');
            document.getElementById('form-success').classList.remove('hidden');
        })
        .finally(function() {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
    });
}

/**
 * Smooth scroll for anchor links
 */
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
