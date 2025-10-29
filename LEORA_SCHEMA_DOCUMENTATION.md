# Leora Home Health - Schema.org & Pydantic Type Definitions

Comprehensive structured data types for the Leora Home Health application, compatible with both Schema.org vocabulary and Pydantic validation.

## Overview

This implementation provides:

1. **Schema.org Compatible Types** - Proper JSON-LD structured data for SEO and semantic web
2. **Pydantic Models** - Type-safe Python objects with validation
3. **Data Loaders** - Utilities to load data from CSV files
4. **Export Functions** - Convert models to JSON-LD format

## Files

- `leora_schema_types.py` - Core type definitions and Pydantic models
- `leora_data_loader.py` - Data loading utilities for CSV files
- `LEORA_SCHEMA_DOCUMENTATION.md` - This documentation file

## Architecture

### Type Hierarchy

```
Thing (Base Schema.org type)
├── Place
│   ├── City
│   └── State
├── Organization
│   └── LocalBusiness
│       └── LeoraHomeHealth
├── Service
└── Product
```

### Core Models

#### 1. LeoraHomeHealth (LocalBusiness)

The main organization model representing Leora Home Health.

```python
from leora_schema_types import create_leora_organization

org = create_leora_organization()
print(org.name)  # "Leora Home Health"
print(org.telephone)  # "+1-512-222-8103"
```

**Schema.org Type**: `LocalBusiness`

**Key Properties**:
- `name`: Organization name
- `description`: Business description
- `url`: Website URL
- `telephone`: Contact phone
- `email`: Contact email
- `address`: PostalAddress object
- `geo`: GeoCoordinates object
- `areaServed`: List of served areas (Cities/States)
- `openingHoursSpecification`: Business hours
- `hasOfferCatalog`: Services offered
- `services`: List of Service objects
- `products`: List of ProductVariant objects
- `categories`: List of ServiceCategory objects

#### 2. Service

Represents a home health service offered by Leora.

```python
from leora_schema_types import Service, ServiceType, State

service = Service(
    schema_id="https://www.leorahomehealth.com/#skilled-nursing",
    name="Skilled Nursing",
    description="Professional nursing care delivered at home",
    serviceType=ServiceType.SKILLED_NURSING,
    areaServed=State(name="Texas")
)
```

**Schema.org Type**: `Service`

**Key Properties**:
- `name`: Service name
- `description`: Service description
- `provider`: Organization providing the service
- `areaServed`: Geographic areas served
- `serviceType`: Type of service (enum)

#### 3. ProductVariant

Represents a service package with pricing tiers.

```python
from leora_schema_types import ProductVariant, ProductTier, PricingDuration
from decimal import Decimal

product = ProductVariant(
    variant_id="6700b1003622e22dbd310f39",
    product_id="6700b1003622e22dbd310e22",
    product_handle="basic",
    product_name="Basic",
    product_type="Advanced",
    tier=ProductTier.BASIC,
    duration=PricingDuration.MONTHLY,
    price=Decimal("2999.00"),
    compare_at_price=Decimal("3999.00")
)
```

**Key Properties**:
- `tier`: BASIC, STANDARD, or LUXURY
- `duration`: MONTHLY or YEARLY
- `price`: Current price
- `compare_at_price`: Original price (for discounts)
- `tax_class`: Tax classification

#### 4. ServiceCategory

Represents a service category.

```python
from leora_schema_types import ServiceCategory

category = ServiceCategory(
    name="Basic",
    slug="basic",
    description="Entry-level home health services",
    collection_id="6700b1003622e22dbd310e23",
    item_id="6700b1003622e22dbd310f4f"
)
```

### Supporting Types

#### PostalAddress

```python
from leora_schema_types import PostalAddress

address = PostalAddress(
    addressLocality="Austin",
    addressRegion="TX",
    addressCountry="US"
)
```

#### GeoCoordinates

```python
from leora_schema_types import GeoCoordinates

geo = GeoCoordinates(
    latitude=30.2672,
    longitude=-97.7431
)
```

#### OpeningHoursSpecification

```python
from leora_schema_types import OpeningHoursSpecification, DayOfWeek

hours = OpeningHoursSpecification(
    dayOfWeek=[DayOfWeek.MONDAY, DayOfWeek.FRIDAY],
    opens="08:00",
    closes="17:00"
)
```

## Data Loading

### Loading from CSV Files

```python
from leora_data_loader import LeoraDataLoader

# Initialize loader with path to Leora codebase
loader = LeoraDataLoader("~/code/IntegrityStudioClients/Leora")

# Load products from CSV
products = loader.load_products()
print(f"Loaded {len(products)} products")

# Load categories from CSV
categories = loader.load_categories()
print(f"Loaded {len(categories)} categories")

# Create complete organization with all data
org = loader.create_complete_organization()
```

### CSV File Structure

**Products File**: `Leora Home Health - Products.csv`
- Contains product variants with pricing tiers (Basic, Standard, Luxury)
- Monthly and Yearly pricing options
- Product metadata and images

**Categories File**: `Leora Home Health - Categories.csv`
- Service category definitions
- Category descriptions and slugs

## JSON-LD Export

### Export Organization

```python
from leora_schema_types import create_leora_organization, export_to_json_ld
import json

org = create_leora_organization()
json_ld = export_to_json_ld(org)

# Pretty print
print(json.dumps(json_ld, indent=2, default=str))

# Save to file
with open('leora_organization.json', 'w') as f:
    json.dump(json_ld, f, indent=2, default=str)
```

### Export Products

```python
from leora_data_loader import LeoraDataLoader, generate_product_json_ld

loader = LeoraDataLoader()
products = loader.load_products()

for product in products:
    json_ld = generate_product_json_ld(product)
    print(json.dumps(json_ld, indent=2, default=str))
```

### Export Complete Data

```python
from leora_data_loader import LeoraDataLoader, export_all_to_json_ld

loader = LeoraDataLoader()
org = loader.create_complete_organization()

# Export everything to JSON-LD
json_ld = export_all_to_json_ld(org, "leora_complete.json")
```

## Validation

All models include Pydantic validation:

```python
from leora_schema_types import PostalAddress
from pydantic import ValidationError

# Valid address
address = PostalAddress(
    addressLocality="Austin",
    addressRegion="TX",
    addressCountry="US"
)

# Invalid - will raise ValidationError
try:
    bad_address = PostalAddress(
        addressLocality="Austin"
        # Missing required fields
    )
except ValidationError as e:
    print(e)
```

## Enumerations

### ServiceType
- `SKILLED_NURSING`
- `HOME_HEALTH_AIDE`
- `PERSONAL_ASSISTANT`
- `MEDICAL_SOCIAL_SERVICES`

### ProductTier
- `BASIC`
- `STANDARD`
- `LUXURY`

### PricingDuration
- `MONTHLY`
- `YEARLY`

### DayOfWeek
- `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`

## Integration with HTML

### Add to HTML `<head>` section

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://www.leorahomehealth.com/#organization",
  "name": "Leora Home Health",
  ...
}
</script>
```

### Generate from Python

```python
from leora_schema_types import create_leora_organization, export_to_json_ld
import json

org = create_leora_organization()
json_ld = export_to_json_ld(org)

# Generate script tag
script = f'''<script type="application/ld+json">
{json.dumps(json_ld, indent=2, default=str)}
</script>'''

print(script)
```

## Schema.org Validation

Validate your JSON-LD using:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

## Examples

### Example 1: Create Basic Organization

```python
from leora_schema_types import create_leora_organization

org = create_leora_organization()
print(f"Organization: {org.name}")
print(f"Services: {len(org.services)}")
print(f"Opening Hours: {org.openingHoursSpecification[0].opens}")
```

### Example 2: Load and Display Products

```python
from leora_data_loader import LeoraDataLoader

loader = LeoraDataLoader()
products = loader.load_products()

for product in products:
    print(f"{product.product_name} - {product.duration.value}")
    print(f"  Price: ${product.price}")
    print(f"  Was: ${product.compare_at_price}")
    print()
```

### Example 3: Export for Website

```python
from leora_data_loader import LeoraDataLoader, export_all_to_json_ld
import json

# Load all data
loader = LeoraDataLoader()
org = loader.create_complete_organization()

# Export to JSON-LD for website
json_ld = export_to_json_ld(org)

# Generate HTML script tag
html_script = f'''
<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{json.dumps(json_ld, indent=2, default=str)}
</script>
'''

print(html_script)
```

## Benefits

### 1. SEO Optimization
- Rich snippets in Google search results
- Better understanding by search engines
- Improved local search visibility

### 2. Type Safety
- Pydantic validation catches errors early
- IDE autocomplete support
- Clear type hints

### 3. Semantic Web
- Machine-readable structured data
- Interoperability with other systems
- Future-proof data model

### 4. Maintainability
- Single source of truth for data structure
- Easy to update and extend
- Well-documented types

## Dependencies

```bash
pip install pydantic
```

## License

This code is part of the Leora Home Health project and should follow the same licensing as the main codebase.

## Support

For questions or issues, refer to:
- Schema.org documentation: https://schema.org/
- Pydantic documentation: https://pydantic-docs.helpmanual.io/
- Leora Home Health codebase: ~/code/IntegrityStudioClients/Leora

## Notes

⚠️ **Security Notice**: As noted in the Leora README, the current application has security vulnerabilities and is not production-ready. These type definitions are independent of those security concerns but should be used within a secure backend implementation.
