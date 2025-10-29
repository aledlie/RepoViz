"""
Luis Landscaping & Handyman Services - Data Loader Utilities

This module provides utilities to load data from the Luis Landscaping codebase
and convert it into structured Pydantic models with schema.org compatibility.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from luis_landscaping_schema_types import (
    ContactFormData,
    LuisLandscapingBusiness,
    LuisLandscapingService,
    create_luis_landscaping_business,
    export_to_json_ld,
    ContactType,
    ServiceType
)


class LuisLandscapingDataLoader:
    """Loads and manages Luis Landscaping data"""

    def __init__(self, base_path: str = "~/code/IntegrityStudioClients/luis-landscaping"):
        """
        Initialize the data loader

        Args:
            base_path: Path to the Luis Landscaping codebase root directory
        """
        self.base_path = Path(base_path).expanduser()

    def load_business_config(self) -> Dict[str, Any]:
        """
        Load business configuration from TypeScript config file

        Returns:
            Dictionary containing business configuration data
        """
        config_path = self.base_path / "src" / "config" / "business.ts"

        if not config_path.exists():
            print(f"Config file not found: {config_path}")
            return {}

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse TypeScript object (simple extraction)
            # Look for businessInfo object
            config_data = {
                "name": self._extract_value(content, "name"),
                "address": self._extract_value(content, "address"),
                "city": self._extract_value(content, "city"),
                "state": self._extract_value(content, "state"),
                "zip": self._extract_value(content, "zip"),
                "phone": self._extract_value(content, "phone"),
                "email": self._extract_value(content, "email"),
                "services": self._extract_services(content)
            }

            return config_data

        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def _extract_value(self, content: str, key: str) -> Optional[str]:
        """
        Extract a simple string value from TypeScript config

        Args:
            content: TypeScript file content
            key: Key to extract

        Returns:
            Extracted value or None
        """
        import re

        # Look for key: 'value' or key: "value"
        pattern = rf"{key}:\s*['\"]([^'\"]+)['\"]"
        match = re.search(pattern, content)

        if match:
            return match.group(1)

        return None

    def _extract_services(self, content: str) -> List[str]:
        """
        Extract services array from TypeScript config

        Args:
            content: TypeScript file content

        Returns:
            List of service names
        """
        import re

        # Look for services: ['Service 1', 'Service 2', ...]
        pattern = r"services:\s*\[(.*?)\]"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return []

        services_str = match.group(1)

        # Extract quoted strings
        service_pattern = r"['\"]([^'\"]+)['\"]"
        services = re.findall(service_pattern, services_str)

        return services

    def create_sample_contact_forms(self, count: int = 5) -> List[ContactFormData]:
        """
        Create sample contact form submissions for testing

        Args:
            count: Number of sample forms to create

        Returns:
            List of ContactFormData objects
        """
        forms = []
        contact_types = [
            ContactType.GENERAL_INQUIRY,
            ContactType.SERVICE_REQUEST,
            ContactType.QUOTE_REQUEST,
            ContactType.FEEDBACK
        ]

        for i in range(count):
            form = ContactFormData(
                name=f"Sample Customer {i+1}",
                email=f"customer{i+1}@example.com",
                phone=f"(512) 555-{1000 + i:04d}",
                message=f"Sample inquiry #{i+1} about landscaping services",
                contact_type=contact_types[i % len(contact_types)],
                submitted_at=datetime.now()
            )
            forms.append(form)

        return forms

    def create_complete_business(self) -> LuisLandscapingBusiness:
        """
        Create a complete LuisLandscapingBusiness with all data

        Returns:
            LuisLandscapingBusiness object
        """
        return create_luis_landscaping_business()

    def export_business_to_json_ld(
        self,
        business: LuisLandscapingBusiness,
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export business to JSON-LD format

        Args:
            business: LuisLandscapingBusiness object
            output_file: Optional file path to save JSON-LD

        Returns:
            Dictionary representing JSON-LD
        """
        json_ld = export_to_json_ld(business)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_ld, f, indent=2, default=str)
            print(f"JSON-LD exported to: {output_file}")

        return json_ld

    def generate_graph_json_ld(
        self,
        business: LuisLandscapingBusiness
    ) -> Dict[str, Any]:
        """
        Generate full @graph JSON-LD for Luis Landscaping

        Args:
            business: LuisLandscapingBusiness object

        Returns:
            Dictionary with @context and @graph
        """
        from luis_landscaping_schema_types import (
            Service,
            WebSite,
            SearchAction,
            EntryPoint
        )

        # Create website structure
        website = WebSite(
            schema_id="https://luislandscaping.com/#website",
            schema_type="WebSite",
            url="https://luislandscaping.com/",
            name="Luis Landscaping & Handyman Services",
            description="Professional landscaping and handyman services in Austin, TX",
            publisher={"@id": "https://luislandscaping.com/#business"},
            potentialAction=SearchAction(
                target=EntryPoint(
                    urlTemplate="https://luislandscaping.com/?s={search_term_string}"
                ),
                query_input="required name=search_term_string"
            )
        )

        # Build graph
        graph_items = [
            export_to_json_ld(business),
        ]

        # Add all services
        for service in business.services:
            graph_items.append(export_to_json_ld(service))

        # Add website structure
        graph_items.append(export_to_json_ld(website))

        return {
            "@context": "https://schema.org",
            "@graph": graph_items
        }

    def validate_contact_form(self, form_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Validate contact form data

        Args:
            form_data: Dictionary with form fields

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Required fields
        required = ["name", "email", "phone", "message"]
        for field in required:
            if field not in form_data or not form_data[field]:
                errors.append({
                    "field": field,
                    "message": f"{field.capitalize()} is required"
                })

        # Email validation (basic)
        if "email" in form_data and form_data["email"]:
            if "@" not in form_data["email"]:
                errors.append({
                    "field": "email",
                    "message": "Invalid email format"
                })

        # Phone validation
        if "phone" in form_data and form_data["phone"]:
            phone = form_data["phone"]
            cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            if not cleaned.isdigit() or len(cleaned) < 10:
                errors.append({
                    "field": "phone",
                    "message": "Invalid phone number"
                })

        return errors


def generate_html_script_tag(json_ld: Dict[str, Any]) -> str:
    """
    Generate HTML script tag with JSON-LD

    Args:
        json_ld: JSON-LD dictionary

    Returns:
        HTML script tag as string
    """
    json_str = json.dumps(json_ld, indent=2, default=str)
    return f'''<!-- Structured Data -->
<script type="application/ld+json">
{json_str}
</script>'''


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import json

    # Initialize loader
    loader = LuisLandscapingDataLoader()

    print("\n=== Loading Business Config from TypeScript ===")
    try:
        config = loader.load_business_config()
        if config:
            print(f"Loaded config for: {config.get('name', 'Unknown')}")
            print(f"  Address: {config.get('address', '')}, {config.get('city', '')}, {config.get('state', '')}")
            print(f"  Phone: {config.get('phone', '')}")
            print(f"  Services: {len(config.get('services', []))}")
            for svc in config.get('services', []):
                print(f"    - {svc}")
        else:
            print("Could not load config (may not exist in this location)")
    except Exception as e:
        print(f"Error: {e}")

    print("\n\n=== Creating Sample Contact Forms ===")
    forms = loader.create_sample_contact_forms(3)
    print(f"Created {len(forms)} sample contact forms")

    for i, form in enumerate(forms):
        print(f"\n  Form {i+1}: {form.name}")
        print(f"    Email: {form.email}")
        print(f"    Phone: {form.phone}")
        print(f"    Type: {form.contact_type}")

    print("\n\n=== Creating Complete Business ===")
    business = loader.create_complete_business()
    print(f"Business: {business.name}")
    print(f"  Phone: {business.telephone}")
    print(f"  Services: {len(business.services)}")
    print(f"  Address: {business.address.street_address if business.address else 'N/A'}")

    print("\n\n=== Service Details ===")
    for service in business.services:
        print(f"\n  {service.name}")
        print(f"    Type: {service.service_type}")
        print(f"    Description: {service.description[:80]}...")

    print("\n\n=== Exporting to JSON-LD ===")
    json_ld = loader.export_business_to_json_ld(business, "luis_landscaping_business.json")

    print("\n\n=== Generating Full Graph JSON-LD ===")
    graph_json_ld = loader.generate_graph_json_ld(business)
    print(f"Generated @graph with {len(graph_json_ld['@graph'])} items")

    # Save graph
    with open("luis_landscaping_graph.json", "w") as f:
        json.dump(graph_json_ld, f, indent=2, default=str)
    print("Full graph saved to: luis_landscaping_graph.json")

    # Generate HTML script tag
    print("\n\n=== Sample HTML Script Tag ===")
    script_tag = generate_html_script_tag(graph_json_ld)
    print(script_tag[:500] + "...")

    print("\n\n=== Validating Sample Form ===")
    sample_form = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "(512) 555-1234",
        "message": "I need landscaping services"
    }
    errors = loader.validate_contact_form(sample_form)
    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"  {error['field']}: {error['message']}")
    else:
        print("✓ Form validation passed")

    print("\n\n=== Business Information Summary ===")
    print(f"Name: {business.name}")
    print(f"Phone: {business.telephone}")
    if business.address:
        print(f"Address: {business.address.street_address}")
        print(f"         {business.address.address_locality}, {business.address.address_region} {business.address.postal_code}")
    if business.opening_hours_specification:
        print(f"Hours: {len(business.opening_hours_specification)} schedules defined")
    if business.area_served:
        print(f"Service Area: {', '.join(business.area_served) if isinstance(business.area_served, list) else business.area_served}")
