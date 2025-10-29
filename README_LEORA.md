# Leora Home Health - Schema.org & Pydantic Type System

A complete implementation of structured data types for the Leora Home Health application, providing schema.org compatible JSON-LD output with Pydantic validation.

## Quick Start

```python
from leora_data_loader import LeoraDataLoader

# Load all data from the Leora codebase
loader = LeoraDataLoader("~/code/IntegrityStudioClients/Leora")
org = loader.create_complete_organization()

# Export to JSON-LD
from leora_data_loader import export_all_to_json_ld
export_all_to_json_ld(org, "output.json")
```

## Files

| File | Description | Size |
|------|-------------|------|
| `leora_schema_types.py` | Core Pydantic models & Schema.org types | 17KB |
| `leora_data_loader.py` | CSV data loader & JSON-LD exporter | 11KB |
| `LEORA_SCHEMA_DOCUMENTATION.md` | Complete usage documentation | 9.7KB |
| `LEORA_IMPLEMENTATION_SUMMARY.md` | Implementation details & analysis | 9.0KB |
| `leora_complete.json` | Sample JSON-LD output | 12KB |
| `README_LEORA.md` | This file | - |

## What's Included

### Schema.org Types (15+)
- LocalBusiness, Organization, Service, Product, Offer
- PostalAddress, GeoCoordinates, City, State
- OpeningHoursSpecification, OfferCatalog
- And more...

### Domain Models
- **LeoraHomeHealth**: Complete organization model
- **ProductVariant**: Service packages with pricing tiers
- **ServiceCategory**: Service categorization
- **ContactInformation**: Contact details with validation

### Data Loading
- Parse products from CSV (6 variants)
- Parse categories from CSV (3 categories)
- Automatic type conversion and validation

### JSON-LD Export
- Valid schema.org JSON-LD output
- Circular reference handling
- Pretty printing support

## Usage

### 1. Create Organization Manually

```python
from leora_schema_types import create_leora_organization, export_to_json_ld

org = create_leora_organization()
json_ld = export_to_json_ld(org)
```

### 2. Load from CSV Files

```python
from leora_data_loader import LeoraDataLoader

loader = LeoraDataLoader()
products = loader.load_products()      # 6 products
categories = loader.load_categories()  # 3 categories
```

### 3. Generate Complete JSON-LD

```python
org = loader.create_complete_organization()
json_ld = export_all_to_json_ld(org, "leora_complete.json")
```

### 4. Individual Product JSON-LD

```python
from leora_data_loader import generate_product_json_ld

products = loader.load_products()
product_json = generate_product_json_ld(products[0])
```

## Test the Implementation

```bash
# Test type definitions
python leora_schema_types.py

# Test data loading
python leora_data_loader.py
```

Both scripts will output sample JSON-LD to demonstrate functionality.

## Integration with HTML

Add the generated JSON-LD to your HTML `<head>` section:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  ...
}
</script>
```

## Key Features

✅ **Schema.org Compliant** - Valid JSON-LD for SEO
✅ **Type Safe** - Pydantic validation prevents errors
✅ **Data Loading** - Parse CSV files automatically
✅ **Well Documented** - Comprehensive docs included
✅ **Tested** - All functionality verified
✅ **Extensible** - Easy to add new types

## Data Structure

```
LeoraHomeHealth (LocalBusiness)
├── Contact Information (phone, email, social)
├── Location (Austin, TX with coordinates)
├── Opening Hours (Mon-Fri, 8:00-17:00)
├── Services (4)
│   ├── Skilled Nursing
│   ├── Home Health Aide (HHA)
│   ├── Personal Assistant Services (PAS)
│   └── Medical Social Services
├── Products (6 variants)
│   ├── Basic (Monthly/Yearly)
│   ├── Standard (Monthly/Yearly)
│   └── Luxury (Monthly/Yearly)
└── Categories (3)
    ├── Basic
    ├── Standard
    └── Luxury
```

## Dependencies

```bash
pip install pydantic
```

## Documentation

- **Full Documentation**: See `LEORA_SCHEMA_DOCUMENTATION.md`
- **Implementation Details**: See `LEORA_IMPLEMENTATION_SUMMARY.md`
- **Schema.org Reference**: https://schema.org/
- **Pydantic Docs**: https://docs.pydantic.dev/

## Output Example

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://www.leorahomehealth.com/#organization",
  "name": "Leora Home Health",
  "telephone": "+1-512-222-8103",
  "email": "appointments@leorahomehealth.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "addressCountry": "US"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Home Health Services",
    "itemListElement": [...]
  }
}
```

## Validation

Validate your JSON-LD output:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

## Benefits

**SEO**: Rich snippets, better search rankings, Knowledge Graph integration
**Quality**: Type safety, validation, consistent structure
**Maintainability**: Single source of truth, well-documented
**Interoperability**: Standard vocabulary, machine-readable

## Source Codebase

Original codebase analyzed: `~/code/IntegrityStudioClients/Leora`

## License

This implementation should follow the same licensing as the Leora Home Health project.

---

**Created**: October 29, 2025
**Status**: ✅ Complete and tested
**Python**: 3.12+
**Pydantic**: 2.x
