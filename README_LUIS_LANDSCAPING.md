# Luis Landscaping & Handyman Services - Schema.org & Pydantic Type System

A complete implementation of structured data types for Luis Landscaping & Handyman Services, providing schema.org compatible JSON-LD output with Pydantic validation.

## Quick Start

```python
from luis_landscaping_data_loader import LuisLandscapingDataLoader

# Initialize loader
loader = LuisLandscapingDataLoader()

# Create complete business model
business = loader.create_complete_business()

# Generate full @graph JSON-LD
graph = loader.generate_graph_json_ld(business)

# Export to file
loader.export_business_to_json_ld(business, "output.json")
```

## Files

| File | Description | Size |
|------|-------------|------|
| `luis_landscaping_schema_types.py` | Core Pydantic models & Schema.org types | ~500 LOC |
| `luis_landscaping_data_loader.py` | TypeScript config parser & JSON-LD generator | ~350 LOC |
| `LUIS_LANDSCAPING_IMPLEMENTATION_SUMMARY.md` | Complete implementation details | ~400 lines |
| `README_LUIS_LANDSCAPING.md` | This file | - |

## What's Included

### Schema.org Types (15+)
- LocalBusiness, Service
- PostalAddress, GeoCoordinates, Place
- OpeningHoursSpecification
- Offer, OfferCatalog
- ContactPoint
- WebSite, SearchAction, EntryPoint

### Service Types (Enum)
- Tree Service
- Landscaping
- Lawn Maintenance
- Handyman Services
- Garden Services

### Contact Form Management
- ContactFormData with validation
- Contact types (General Inquiry, Service Request, Quote Request, Feedback)
- Phone and email validation

### Data Loading
- Parse TypeScript configuration files
- Generate sample contact form submissions
- Create full @graph JSON-LD
- HTML script tag generation

## Usage

### 1. Create Business Manually

```python
from luis_landscaping_schema_types import (
    create_luis_landscaping_business,
    export_to_json_ld
)

business = create_luis_landscaping_business()
json_ld = export_to_json_ld(business)
```

### 2. Load from TypeScript Config

```python
from luis_landscaping_data_loader import LuisLandscapingDataLoader

loader = LuisLandscapingDataLoader()

# Load business config
config = loader.load_business_config()
print(f"Business: {config['name']}")
print(f"Services: {config['services']}")
```

### 3. Generate Complete @Graph

```python
# Create business
business = loader.create_complete_business()

# Generate full @graph with all schema.org types
graph_json_ld = loader.generate_graph_json_ld(business)

# Save to file
import json
with open("schema.json", "w") as f:
    json.dump(graph_json_ld, f, indent=2, default=str)
```

### 4. Create Sample Contact Forms

```python
# Generate sample contact forms
forms = loader.create_sample_contact_forms(count=5)

for form in forms:
    print(f"{form.name}: {form.email} - {form.contact_type}")
```

### 5. Validate Contact Form Data

```python
# Validate form submission
form_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(512) 555-1234",
    "message": "Need landscaping help"
}

errors = loader.validate_contact_form(form_data)
if not errors:
    print("✓ Valid form")
```

### 6. Generate HTML Script Tag

```python
from luis_landscaping_data_loader import generate_html_script_tag

# Get complete graph
graph = loader.generate_graph_json_ld(business)

# Generate HTML
html_tag = generate_html_script_tag(graph)
print(html_tag)
```

## Test the Implementation

```bash
# Test type definitions
python luis_landscaping_schema_types.py

# Test data loading
python luis_landscaping_data_loader.py
```

## Key Features

✅ **Schema.org Compliant** - Valid JSON-LD with @graph
✅ **Type Safe** - Pydantic validation
✅ **TypeScript Config Parsing** - Load existing business config
✅ **Contact Form Validation** - Phone and email validation
✅ **Sample Data** - Generate test data
✅ **Well Documented** - Comprehensive docs
✅ **Tested** - All functionality verified

## Data Structure

```
LuisLandscapingBusiness (LocalBusiness)
├── Basic Info
│   ├── Name: "Luis Landscaping & Handyman Services"
│   ├── Phone: (737) 420-7339
│   └── Location: Austin, TX
├── Address
│   ├── Street: 12028 Timber Heights Drive
│   ├── City: Austin
│   ├── State: TX
│   └── ZIP: 78754
├── Geo Coordinates
│   ├── Latitude: 30.3672
│   └── Longitude: -97.6431
├── Opening Hours
│   ├── Mon-Fri: 7:00 AM - 6:00 PM
│   └── Saturday: 8:00 AM - 3:00 PM
├── Services (5)
│   ├── Tree Service
│   ├── Landscaping
│   ├── Lawn Maintenance
│   ├── Handyman Services
│   └── Garden Services
└── Service Area
    ├── Austin, TX
    ├── Round Rock, TX
    ├── Cedar Park, TX
    └── Pflugerville, TX
```

## Service Catalog

| Service | Description | Type |
|---------|-------------|------|
| Tree Service | Professional tree trimming, pruning, and removal | Tree Service |
| Landscaping | Complete landscaping design and installation | Landscaping |
| Lawn Maintenance | Regular lawn mowing, edging, and trimming | Lawn Maintenance |
| Handyman Services | General home repairs and installations | Handyman Services |
| Garden Services | Garden design, planting, and maintenance | Garden Services |

## Business Information

**Name**: Luis Landscaping & Handyman Services
**Phone**: (737) 420-7339
**Address**: 12028 Timber Heights Drive, Austin, TX 78754
**Service Area**: Austin, Round Rock, Cedar Park, Pflugerville
**Price Range**: $$
**Hours**: Mon-Fri 7am-6pm, Sat 8am-3pm

## Dependencies

```bash
pip install pydantic
```

Optional (for email validation):
```bash
pip install 'pydantic[email]'
```

## JSON-LD Output Example

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "@id": "https://luislandscaping.com/#business",
      "name": "Luis Landscaping & Handyman Services",
      "telephone": "(737) 420-7339",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "12028 Timber Heights Drive",
        "addressLocality": "Austin",
        "addressRegion": "TX",
        "postalCode": "78754"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 30.3672,
        "longitude": -97.6431
      },
      "priceRange": "$$",
      "areaServed": [
        "Austin, TX",
        "Round Rock, TX",
        "Cedar Park, TX",
        "Pflugerville, TX"
      ]
    },
    {
      "@type": "Service",
      "@id": "https://luislandscaping.com/#service-tree",
      "name": "Tree Service",
      "serviceType": "Tree Service"
    }
    // ... more services
  ]
}
```

## Validation

Validate your JSON-LD output:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

## Benefits

**SEO**: Rich snippets, better rankings, local business visibility
**Quality**: Type safety, validation, consistency
**Maintainability**: Single source of truth, documented
**Integration**: TypeScript config + Schema.org
**Flexibility**: Sample data generation, form validation

## Source Codebase

Original codebase analyzed: `~/code/IntegrityStudioClients/luis-landscaping`

**Tech Stack**:
- TypeScript + Vite
- React components
- Static website
- Contact form integration

## Use Cases

### 1. SEO Enhancement
```python
# Generate schema for website
business = create_luis_landscaping_business()
graph = loader.generate_graph_json_ld(business)
script = generate_html_script_tag(graph)
# Add to HTML <head>
```

### 2. Contact Form Processing
```python
# Validate form submission
errors = loader.validate_contact_form(form_data)
if not errors:
    # Process form
    form = ContactFormData(**form_data)
```

### 3. Testing
```python
# Generate sample data
forms = loader.create_sample_contact_forms(10)
# Use in tests
```

### 4. API Integration
```python
# Export services as JSON
for service in business.services:
    print(f"{service.name}: {service.service_type}")
```

## Documentation

- **Full Implementation Details**: See `LUIS_LANDSCAPING_IMPLEMENTATION_SUMMARY.md`
- **Schema.org Reference**: https://schema.org/
- **Pydantic Docs**: https://docs.pydantic.dev/

## License

This implementation should follow the same licensing as the Luis Landscaping project.

---

**Created**: October 29, 2025
**Status**: ✅ Complete and tested
**Python**: 3.12+
**Pydantic**: 2.x
**Services**: 5 landscaping and handyman services in Austin, TX
