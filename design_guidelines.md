# Design Guidelines: Luxury Private Jet Charter Platform

## Design Approach: Reference-Based (Luxury Aviation)

**Primary Reference:** VistaJet - epitomizing ultra-premium private aviation aesthetics
**Supporting References:** NetJets, Wheels Up for feature patterns

**Core Design Principles:**
- Sophisticated luxury without ostentation
- Spacious, breathable layouts that convey exclusivity
- Rich imagery showcasing aircraft and destinations
- Seamless, invisible technology experience
- Confidence and trust through clarity

---

## Typography System

**Font Selection:**
- **Headings:** Museo Sans (700, 600) - or similar elegant sans-serif (Outfit, Inter Display)
- **Body:** Museo Sans (400, 500) for consistency
- **Accent/Special:** Consider serif for editorial content sections (Lora, Merriweather)

**Type Scale:**
- H1: 64px / 4rem (Hero headlines)
- H2: 48px / 3rem (Section headers)
- H3: 32px / 2rem (Subsections)
- H4: 24px / 1.5rem (Card titles)
- Body Large: 18px / 1.125rem (Intro paragraphs)
- Body: 16px / 1rem (Standard text)
- Small: 14px / 0.875rem (Captions, metadata)

**Hierarchy Rules:**
- Headlines: Tight line-height (1.1-1.2), generous letter-spacing (0.02em)
- Body: Comfortable reading line-height (1.6-1.7)
- Max text width: 65-75 characters (max-w-prose)

---

## Layout System

**Spacing Primitives (Tailwind units):**
- **Micro spacing:** 1, 2, 3 (4px, 8px, 12px) - for tight groupings
- **Standard spacing:** 4, 6, 8 (16px, 24px, 32px) - component internal spacing
- **Section spacing:** 12, 16, 20, 24 (48px, 64px, 80px, 96px) - between major sections
- **Hero/Feature spacing:** 32, 40 (128px, 160px) - dramatic vertical rhythm

**Container Strategy:**
- Full-width hero sections with inner max-w-7xl (1280px)
- Content sections: max-w-6xl (1152px)
- Forms and text-heavy content: max-w-4xl (896px)

**Grid Patterns:**
- 12-column grid foundation
- Common breakouts: 2-column (md), 3-column (lg), 4-column (xl) for features/aircraft
- Asymmetric layouts for visual interest (e.g., 7-5 split for content+image)

---

## Component Library

### Navigation
**Header:**
- Fixed/sticky navigation with glass-morphism effect on scroll
- Multi-level mega-menu for fleet, memberships, destinations
- Prominent CTA button ("Book Flight" or "Get Quote")
- Language/region selector in top-right

**Footer:**
- Comprehensive 4-5 column layout
- Newsletter signup module with generous padding
- Trust indicators (certifications, safety ratings)
- Social proof and contact information

### Flight Booking Widget
**Critical Component** - Featured prominently on homepage hero:
- Multi-step form: Route selection → Date/Time → Passengers → Aircraft preference
- From/To inputs with autocomplete (airport codes)
- Date pickers with return/one-way toggle
- Passenger counter with simple +/- controls
- "Multi-city" option for complex itineraries
- Floating/card design with subtle shadow and blur backdrop when over hero image
- Progress indicator for multi-step flow

### Cards
**Aircraft Cards:**
- Large hero image (16:9 aspect ratio)
- Aircraft name and category overlay
- Key specs (passengers, range, speed) in icon + text format
- "Explore" or "Request Quote" CTA

**Membership Cards:**
- Image-led with overlay gradient for text legibility
- Tier name prominently displayed
- 2-3 key benefits listed
- "Learn More" link

**Service/Feature Cards:**
- Numbered sequence (01, 02, 03) for multi-step services
- Alternating image-left/image-right layout for variety
- Collapsible/expandable details on mobile

### Forms
**Contact/Quote Request:**
- Clean, spacious inputs with floating labels
- Dropdown styling with custom arrows
- Phone number input with country code selector
- Multi-step forms with clear progress indication
- Generous vertical spacing between fields (space-y-6)

### Media Components
**Image Galleries:**
- Full-bleed hero images (viewport height: 70-90vh)
- Before/after slider for aircraft comparisons
- Lightbox for detailed aircraft interior views

**Video Integration:**
- Ambient background video in hero (muted autoplay)
- Play button overlay for feature videos
- Full-screen modal player for testimonials

---

## Animations & Interactions

**Philosophy:** Subtle, purposeful motion that reinforces luxury
- **Scroll-triggered:** Fade-up animations for section reveals (0.6s ease-out)
- **Navigation:** Smooth mega-menu expansion (0.3s)
- **Cards:** Gentle hover lift (translateY: -4px) with shadow increase
- **CTAs:** Scale micro-interaction (scale: 1.02) on hover
- **NO:** Excessive parallax, spinning elements, or jarring transitions

---

## Images

**Hero Section:**
- Full-width, high-quality image of flagship aircraft in flight or on tarmac
- Dramatic lighting (golden hour preferred)
- Blur backdrop (backdrop-blur-sm) for overlaid flight booking widget
- Alternative: Ambient video loop (aircraft taking off, cabin interior)

**Section Images:**
- **Fleet:** Professional photography of each aircraft exterior and luxurious interior
- **Destinations:** Aspirational location imagery (beaches, mountains, cityscapes)
- **Experience:** Lifestyle shots (dining, cabin service, passengers relaxing)
- **Memberships:** Branded aircraft with subtle VistaJet-style red accents

**Aspect Ratios:**
- Hero: 21:9 (ultra-wide) or 16:9
- Aircraft cards: 16:9
- Feature sections: 4:3 or 3:2 for more intimate feel
- Portrait layouts: 3:4 for lifestyle/cabin shots

**Image Treatment:**
- Subtle vignetting on hero images
- Overlay gradients for text legibility (black at 20-40% opacity)
- Maintain natural color grading - avoid over-saturation

---

## Page-Specific Guidelines

### Homepage
**Sections (in order):**
1. **Hero** with flight booking widget overlay
2. **Memberships** (3-column cards showcasing tiers)
3. **Fleet Highlight** (featured aircraft with specs)
4. **Services** (6-item grid or numbered list with alternating images)
5. **Experience** (luxury dining, cabin service, pet-friendly)
6. **Safety & Certifications** (logo grid of accreditations)
7. **Testimonials/News** (rotating carousel or static 3-column)
8. **Final CTA** ("Ready for your trip?" with booking prompt)

### Aircraft Detail Pages
- Full-screen image gallery at top
- Specifications table (range, speed, passengers, baggage)
- Interior layout diagram
- Amenities list with icons
- "Request this aircraft" sticky CTA

### Booking Flow
- Progress bar (Route → Details → Passengers → Quote)
- Persistent sidebar with trip summary
- Aircraft recommendations based on route
- Calendar view for date selection with pricing hints

---

## Accessibility & Best Practices
- Minimum tap target size: 44x44px for all interactive elements
- Focus indicators: 2px outline with brand accent color
- Form validation: Inline error messages below fields
- Alt text for all aircraft and destination images
- Keyboard navigation for mega-menus and booking flow

---

**Implementation Note:** Use Tailwind as primary framework with DaisyUI components as starting points. Customize DaisyUI theme to match VistaJet's sophisticated palette and spacing. Bulma can supplement for specific grid layouts if needed, but prioritize Tailwind for consistency.