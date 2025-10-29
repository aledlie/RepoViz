# Integrity Studio - Schema.org & Pydantic Type System

A complete implementation of structured data types for the Integrity Studio application, providing schema.org compatible JSON-LD output with Pydantic validation.

## Quick Start

```python
from integrity_studio_data_loader import IntegrityStudioDataLoader

# Load existing schema from HTML
loader = IntegrityStudioDataLoader()
org = loader.create_complete_organization()

# Generate full @graph JSON-LD
graph = loader.generate_graph_json_ld(org)

# Export to file
loader.export_organization_to_json_ld(org, "output.json")
```

## Files

| File | Description | Size |
|------|-------------|------|
| `integrity_studio_schema_types.py` | Core Pydantic models & Schema.org types | ~750 LOC |
| `integrity_studio_data_loader.py` | HTML parser & JSON-LD generator | ~400 LOC |
| `INTEGRITY_STUDIO_IMPLEMENTATION_SUMMARY.md` | Complete implementation details | ~450 lines |
| `README_INTEGRITY_STUDIO.md` | This file | - |

## What's Included

### Schema.org Types (25+)
- Organization, Person, Service, ProfessionalService
- PostalAddress, Country, ContactPoint, Audience
- Offer, OfferCatalog, PriceSpecification
- ImageObject
- WebSite, WebPage, BreadcrumbList, SearchAction
- And more...

### Database Models (Prisma)
- **User**: Auth0-integrated user accounts
- **UserProfile**: Extended user information
- **Role**: Role definitions with permissions
- **UserRole**: Role assignments
- **UserSession**: Session tracking
- **UserActivity**: Activity logging

### Domain Models
- **IntegrityStudioOrganization**: Complete org model
- **IntegrityStudioService**: Services with pricing

### Data Loading
- Extract schema.org from HTML
- Generate sample users and roles
- Create full @graph JSON-LD
- HTML script tag generation

## Usage

### 1. Create Organization Manually

```python
from integrity_studio_schema_types import (
    create_integrity_studio_organization,
    export_to_json_ld
)

org = create_integrity_studio_organization()
json_ld = export_to_json_ld(org)
```

### 2. Load from HTML

```python
from integrity_studio_data_loader import IntegrityStudioDataLoader

loader = IntegrityStudioDataLoader()

# Extract existing schema
schema_data = loader.load_schema_from_html()
print(f"Found {len(schema_data.get('@graph', []))} items")

# Extract services
services = loader.extract_services_from_schema(schema_data)
for svc in services:
    print(f"{svc['name']}: ${svc['offers']['priceSpecification']['price']}")
```

### 3. Generate Complete @Graph

```python
# Create organization
org = loader.create_complete_organization()

# Generate full @graph with all schema.org types
graph_json_ld = loader.generate_graph_json_ld(org)

# Save to file
import json
with open("schema.json", "w") as f:
    json.dump(graph_json_ld, f, indent=2, default=str)
```

### 4. Create Sample Database Objects

```python
# Generate sample users
users = loader.create_sample_users(count=5)
for user in users:
    print(f"{user.name}: {user.email}")

# Generate roles
roles = loader.create_sample_roles()
for role in roles:
    print(f"{role.name}: {role.permissions}")
```

### 5. Generate HTML Script Tag

```python
from integrity_studio_data_loader import generate_html_script_tag

# Get complete graph
graph = loader.generate_graph_json_ld(org)

# Generate HTML
html_tag = generate_html_script_tag(graph)
print(html_tag)
```

## Test the Implementation

```bash
# Test type definitions
python integrity_studio_schema_types.py

# Test data loading
python integrity_studio_data_loader.py
```

## Key Features

✅ **Schema.org Compliant** - Valid JSON-LD with @graph
✅ **Type Safe** - Pydantic validation
✅ **Database Models** - Prisma schema support
✅ **HTML Parsing** - Extract existing schema
✅ **Sample Data** - Generate test data
✅ **Well Documented** - Comprehensive docs
✅ **Tested** - All functionality verified

## Data Structure

```
IntegrityStudioOrganization
├── Organization Info
│   ├── Name: "Integrity Studio"
│   ├── Slogan: "Empowering Nonprofits Through AI-Aware Compliance"
│   ├── Founded: 2024
│   └── Location: Austin, TX, USA
├── Founder (Alyshia Ledlie)
│   ├── Title: Founder & AI Consultant
│   └── Expertise: AI, Nonprofit Tech, Compliance
├── Services (6)
│   ├── AI Integration & Automation ($2,500)
│   ├── Compliance & Safety ($3,500)
│   ├── Strategic Growth Planning ($5,000)
│   ├── Impact Measurement ($2,000)
│   ├── Team Training & Support ($1,500)
│   └── Custom Solutions (Custom)
├── Contact
│   ├── Email: hello@integritystudio.ai
│   ├── Phone: +1-512-829-1644
│   └── Calendly: calendly.com/alyshialedlie
└── Knowledge Areas (8)
```

## Service Catalog

| Service | Price | Type |
|---------|-------|------|
| AI Integration & Automation | $2,500 | AI Integration |
| Compliance & Safety | $3,500 | Compliance Consulting |
| Strategic Growth Planning | $5,000 | Strategic Planning |
| Impact Measurement | $2,000 | Analytics & Reporting |
| Team Training & Support | $1,500 | Training & Education |
| Custom Solutions | Custom | Custom Development |

**Total Fixed Pricing**: $16,500

## Database Schema

From Prisma schema.prisma:

### User Management
- **users**: Core user accounts with Auth0
- **user_profiles**: Extended user info
- **roles**: Permission-based roles
- **user_roles**: Role assignments
- **user_sessions**: Active sessions
- **user_activity**: Activity tracking

### Key Features
- UUID primary keys
- Auth0 integration
- JSON metadata fields
- Timestamps
- Indexes for performance

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
      "@type": "Organization",
      "@id": "https://integritystudio.ai/#organization",
      "name": "Integrity Studio",
      "foundingDate": "2024",
      "services": [...]
    },
    {
      "@type": "ProfessionalService",
      "@id": "https://integritystudio.ai/#professional-service",
      "serviceType": "AI Consulting",
      "category": "Technology Consulting"
    },
    {
      "@type": "Service",
      "@id": "https://integritystudio.ai/#service-ai-integration",
      "name": "AI Integration & Automation",
      "offers": {
        "@type": "Offer",
        "price": "2500"
      }
    }
    // ... more items
  ]
}
```

## Validation

Validate your JSON-LD output:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

## Benefits

**SEO**: Rich snippets, better rankings, Knowledge Graph
**Quality**: Type safety, validation, consistency
**Maintainability**: Single source of truth, documented
**Integration**: Database models + Schema.org
**Flexibility**: Sample data generation, HTML parsing

## Source Codebase

Original codebase analyzed: `~/code/ISPublicSites/IntegrityStudio.ai`

**Tech Stack**:
- React 18 + TypeScript
- Vite build tool
- PostgreSQL + Prisma ORM
- Auth0 authentication
- Tinybird analytics
- TailwindCSS
- Vitest + Playwright

## Use Cases

### 1. SEO Enhancement
```python
# Generate schema for website
org = create_integrity_studio_organization()
graph = loader.generate_graph_json_ld(org)
script = generate_html_script_tag(graph)
# Add to HTML <head>
```

### 2. API Documentation
```python
# Export services as JSON
for service in org.services:
    print(f"{service.name}: ${service.price}")
```

### 3. Testing
```python
# Generate sample data
users = loader.create_sample_users(10)
roles = loader.create_sample_roles()
# Use in tests
```

### 4. Data Migration
```python
# Load from HTML
schema = loader.load_schema_from_html()
# Transform and save to database
```

## Documentation

- **Full Implementation Details**: See `INTEGRITY_STUDIO_IMPLEMENTATION_SUMMARY.md`
- **Schema.org Reference**: https://schema.org/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Prisma Docs**: https://www.prisma.io/docs

## License

This implementation should follow the same licensing as the Integrity Studio project.

---

**Created**: October 29, 2025
**Status**: ✅ Complete and tested
**Python**: 3.12+
**Pydantic**: 2.x
**Services**: 6 AI consulting services for nonprofits
