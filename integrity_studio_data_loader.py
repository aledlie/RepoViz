"""
Integrity Studio - Data Loader Utilities

This module provides utilities to load data from the Integrity Studio codebase
and convert it into structured Pydantic models with schema.org compatibility.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from integrity_studio_schema_types import (
    User,
    UserProfile,
    Role,
    UserRole,
    UserSession,
    UserActivity,
    IntegrityStudioOrganization,
    IntegrityStudioService,
    create_integrity_studio_organization,
    export_to_json_ld,
    ActivityType,
    RoleType
)


class IntegrityStudioDataLoader:
    """Loads and manages Integrity Studio data"""

    def __init__(self, base_path: str = "~/code/ISPublicSites/IntegrityStudio.ai"):
        """
        Initialize the data loader

        Args:
            base_path: Path to the Integrity Studio codebase root directory
        """
        self.base_path = Path(base_path).expanduser()

    def load_schema_from_html(self) -> Dict[str, Any]:
        """
        Load schema.org JSON-LD from the index.html file

        Returns:
            Dictionary containing the schema.org data
        """
        index_path = self.base_path / "index.html"

        if not index_path.exists():
            raise FileNotFoundError(f"Index file not found: {index_path}")

        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract JSON-LD from HTML
        start_marker = '<script type="application/ld+json">'
        end_marker = '</script>'

        start_idx = content.find(start_marker)
        if start_idx == -1:
            return {}

        start_idx += len(start_marker)
        end_idx = content.find(end_marker, start_idx)

        if end_idx == -1:
            return {}

        json_ld_str = content[start_idx:end_idx].strip()

        try:
            return json.loads(json_ld_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON-LD: {e}")
            return {}

    def create_sample_users(self, count: int = 5) -> List[User]:
        """
        Create sample user data for testing

        Args:
            count: Number of sample users to create

        Returns:
            List of User objects
        """
        users = []

        for i in range(count):
            user = User(
                id=uuid4(),
                auth0_id=f"auth0|sample{i}",
                email=f"user{i}@example.com",
                email_verified=True,
                name=f"Sample User {i}",
                nickname=f"user{i}",
                picture=f"https://example.com/avatar{i}.jpg",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now(),
                login_count=i * 5,
                blocked=False,
                metadata={"sample": True, "index": i}
            )
            users.append(user)

        return users

    def create_sample_roles(self) -> List[Role]:
        """
        Create sample role data

        Returns:
            List of Role objects
        """
        roles = [
            Role(
                id=uuid4(),
                name=RoleType.ADMIN.value,
                description="Administrator with full access",
                permissions=["read", "write", "delete", "admin"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Role(
                id=uuid4(),
                name=RoleType.CONSULTANT.value,
                description="AI Consultant with client management access",
                permissions=["read", "write", "manage_clients"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Role(
                id=uuid4(),
                name=RoleType.CLIENT.value,
                description="Client with limited access to their data",
                permissions=["read", "update_profile"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Role(
                id=uuid4(),
                name=RoleType.USER.value,
                description="Standard user with basic access",
                permissions=["read"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]

        return roles

    def create_complete_organization(self) -> IntegrityStudioOrganization:
        """
        Create a complete IntegrityStudioOrganization with all data

        Returns:
            IntegrityStudioOrganization object
        """
        return create_integrity_studio_organization()

    def extract_services_from_schema(self, schema_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract service definitions from schema.org @graph

        Args:
            schema_data: Schema.org JSON-LD data

        Returns:
            List of service dictionaries
        """
        if "@graph" not in schema_data:
            return []

        services = []
        for item in schema_data["@graph"]:
            if item.get("@type") == "Service":
                services.append(item)

        return services

    def export_organization_to_json_ld(
        self,
        org: IntegrityStudioOrganization,
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export organization to JSON-LD format

        Args:
            org: IntegrityStudioOrganization object
            output_file: Optional file path to save JSON-LD

        Returns:
            Dictionary representing JSON-LD
        """
        json_ld = export_to_json_ld(org)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_ld, f, indent=2, default=str)
            print(f"JSON-LD exported to: {output_file}")

        return json_ld

    def generate_graph_json_ld(
        self,
        org: IntegrityStudioOrganization
    ) -> Dict[str, Any]:
        """
        Generate full @graph JSON-LD like the one in index.html

        Args:
            org: IntegrityStudioOrganization object

        Returns:
            Dictionary with @context and @graph
        """
        from integrity_studio_schema_types import (
            ProfessionalService,
            WebSite,
            WebPage,
            BreadcrumbList,
            ListItem,
            SearchAction,
            EntryPoint,
            Audience
        )

        # Create professional service
        professional_service = ProfessionalService(
            schema_id="https://integritystudio.ai/#professional-service",
            schema_type="ProfessionalService",
            name="Integrity Studio - AI Consultancy for Nonprofits",
            url="https://integritystudio.ai/",
            provider={"@id": "https://integritystudio.ai/#organization"},
            serviceType="AI Consulting",
            category="Technology Consulting",
            areaServed={"@type": "Country", "name": "United States"},
            audience=Audience(
                audienceType="Nonprofit Organizations",
                name="Mission-driven organizations and nonprofits"
            ),
            hasOfferCatalog=org.has_offer_catalog
        )

        # Create website
        website = WebSite(
            schema_id="https://integritystudio.ai/#website",
            schema_type="WebSite",
            url="https://integritystudio.ai/",
            name="Integrity Studio",
            description="AI Consultancy for Nonprofits - Empowering mission-driven organizations through ethical AI implementation",
            publisher={"@id": "https://integritystudio.ai/#organization"},
            potentialAction=SearchAction(
                target=EntryPoint(
                    urlTemplate="https://integritystudio.ai/?s={search_term_string}"
                ),
                query_input="required name=search_term_string"
            )
        )

        # Create webpage
        webpage = WebPage(
            schema_id="https://integritystudio.ai/#webpage",
            schema_type="WebPage",
            url="https://integritystudio.ai/",
            name="Integrity Studio - AI Consultancy for Nonprofits",
            isPartOf={"@id": "https://integritystudio.ai/#website"},
            about={"@id": "https://integritystudio.ai/#organization"},
            description="Empowering nonprofits through innovative AI solutions, compliance, and strategic growth planning",
            breadcrumb={"@id": "https://integritystudio.ai/#breadcrumb"}
        )

        # Create breadcrumb
        breadcrumb = BreadcrumbList(
            schema_id="https://integritystudio.ai/#breadcrumb",
            itemListElement=[
                ListItem(
                    position=1,
                    name="Home",
                    item="https://integritystudio.ai/"
                )
            ]
        )

        # Build graph
        graph_items = [
            export_to_json_ld(org),
            export_to_json_ld(professional_service),
        ]

        # Add all services
        for service in org.services:
            graph_items.append(export_to_json_ld(service))

        # Add website structures
        graph_items.extend([
            export_to_json_ld(website),
            export_to_json_ld(webpage),
            export_to_json_ld(breadcrumb)
        ])

        return {
            "@context": "https://schema.org",
            "@graph": graph_items
        }


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
    loader = IntegrityStudioDataLoader()

    print("\n=== Loading Schema from HTML ===")
    try:
        schema_data = loader.load_schema_from_html()
        print(f"Loaded schema.org data with {len(schema_data.get('@graph', []))} items")

        # Extract services
        services = loader.extract_services_from_schema(schema_data)
        print(f"Found {len(services)} services in schema")

        for svc in services[:3]:
            print(f"\n  Service: {svc.get('name')}")
            if 'offers' in svc and 'priceSpecification' in svc['offers']:
                price = svc['offers']['priceSpecification'].get('price', 'Custom')
                print(f"    Price: ${price}")

    except Exception as e:
        print(f"Could not load HTML: {e}")

    print("\n\n=== Creating Sample Users ===")
    users = loader.create_sample_users(3)
    print(f"Created {len(users)} sample users")

    for user in users:
        print(f"\n  User: {user.name}")
        print(f"    Email: {user.email}")
        print(f"    Login count: {user.login_count}")

    print("\n\n=== Creating Sample Roles ===")
    roles = loader.create_sample_roles()
    print(f"Created {len(roles)} roles")

    for role in roles:
        print(f"\n  Role: {role.name}")
        print(f"    Permissions: {', '.join(role.permissions or [])}")

    print("\n\n=== Creating Complete Organization ===")
    org = loader.create_complete_organization()
    print(f"Organization: {org.name}")
    print(f"  Services: {len(org.services)}")
    print(f"  Email: {org.email}")
    print(f"  Telephone: {org.telephone}")

    print("\n\n=== Exporting to JSON-LD ===")
    json_ld = loader.export_organization_to_json_ld(org, "integrity_studio_org.json")

    print("\n\n=== Generating Full Graph JSON-LD ===")
    graph_json_ld = loader.generate_graph_json_ld(org)
    print(f"Generated @graph with {len(graph_json_ld['@graph'])} items")

    # Save graph
    with open("integrity_studio_graph.json", "w") as f:
        json.dump(graph_json_ld, f, indent=2, default=str)
    print("Full graph saved to: integrity_studio_graph.json")

    # Generate HTML script tag
    print("\n\n=== Sample HTML Script Tag ===")
    script_tag = generate_html_script_tag(graph_json_ld)
    print(script_tag[:500] + "...")

    print("\n\n=== Service Pricing Summary ===")
    for service in org.services:
        price_str = f"${service.price}" if service.price else service.price_description or "Contact"
        print(f"  {service.name}: {price_str}")
