"""
Integrity Studio - Schema.org Compatible Type Definitions with Pydantic Models

This module defines structured data types for the Integrity Studio application
that are compatible with both Schema.org vocabulary and Pydantic validation.

Based on analysis of: ~/code/ISPublicSites/IntegrityStudio.ai
"""

from typing import Optional, List, Literal, Union
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from enum import Enum
from uuid import UUID

# EmailStr requires email-validator package
# For simplicity, we'll use str for email addresses
# To enable email validation, install: pip install 'pydantic[email]'
EmailStr = str


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ServiceType(str, Enum):
    """Types of AI services offered"""
    AI_INTEGRATION = "AI Integration"
    COMPLIANCE = "Compliance Consulting"
    STRATEGIC_PLANNING = "Strategic Planning"
    ANALYTICS_REPORTING = "Analytics and Reporting"
    TRAINING_EDUCATION = "Training and Education"
    CUSTOM_DEVELOPMENT = "Custom Development"


class ActivityType(str, Enum):
    """User activity types"""
    LOGIN = "login"
    LOGOUT = "logout"
    PAGE_VIEW = "page_view"
    SERVICE_INQUIRY = "service_inquiry"
    CONTACT_FORM = "contact_form"
    DOWNLOAD = "download"


class RoleType(str, Enum):
    """User role types"""
    ADMIN = "admin"
    USER = "user"
    CONSULTANT = "consultant"
    CLIENT = "client"


# ============================================================================
# SCHEMA.ORG BASE TYPES
# ============================================================================

class Thing(BaseModel):
    """
    Base Schema.org Thing type
    https://schema.org/Thing
    """
    schema_context: str = Field(default="https://schema.org", alias="@context")
    schema_type: str = Field(alias="@type")
    schema_id: Optional[HttpUrl] = Field(default=None, alias="@id")
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    image: Optional[Union[HttpUrl, List[HttpUrl]]] = None

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


# ============================================================================
# PLACE & ADDRESS TYPES
# ============================================================================

class PostalAddress(BaseModel):
    """
    Schema.org PostalAddress
    https://schema.org/PostalAddress
    """
    schema_type: Literal["PostalAddress"] = Field(default="PostalAddress", alias="@type")
    street_address: Optional[str] = Field(default=None, alias="streetAddress")
    address_locality: str = Field(alias="addressLocality")
    address_region: str = Field(alias="addressRegion")
    postal_code: Optional[str] = Field(default=None, alias="postalCode")
    address_country: str = Field(alias="addressCountry")

    model_config = ConfigDict(populate_by_name=True)


class Country(BaseModel):
    """
    Schema.org Country
    https://schema.org/Country
    """
    schema_type: Literal["Country"] = Field(default="Country", alias="@type")
    name: str

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# PERSON & CONTACT TYPES
# ============================================================================

class Person(Thing):
    """
    Schema.org Person
    https://schema.org/Person
    """
    schema_type: Literal["Person"] = Field(default="Person", alias="@type")
    job_title: Optional[str] = Field(default=None, alias="jobTitle")
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    works_for: Optional[Union[dict, "Organization"]] = Field(default=None, alias="worksFor")
    knows_about: Optional[List[str]] = Field(default=None, alias="knowsAbout")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class ContactPoint(BaseModel):
    """
    Schema.org ContactPoint
    https://schema.org/ContactPoint
    """
    schema_type: Literal["ContactPoint"] = Field(default="ContactPoint", alias="@type")
    telephone: str
    email: Optional[EmailStr] = None
    contact_type: str = Field(alias="contactType")
    area_served: Optional[str] = Field(default=None, alias="areaServed")
    available_language: Optional[List[str]] = Field(default=None, alias="availableLanguage")

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# IMAGE TYPES
# ============================================================================

class ImageObject(BaseModel):
    """
    Schema.org ImageObject
    https://schema.org/ImageObject
    """
    schema_type: Literal["ImageObject"] = Field(default="ImageObject", alias="@type")
    url: HttpUrl
    width: Optional[int] = None
    height: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# PRICING & OFFER TYPES
# ============================================================================

class PriceSpecification(BaseModel):
    """
    Schema.org PriceSpecification
    https://schema.org/PriceSpecification
    """
    schema_type: Literal["PriceSpecification"] = Field(default="PriceSpecification", alias="@type")
    price_currency: str = Field(alias="priceCurrency")
    price: Optional[str] = None
    value_added_tax_included: bool = Field(default=False, alias="valueAddedTaxIncluded")
    description: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class Offer(BaseModel):
    """
    Schema.org Offer
    https://schema.org/Offer
    """
    schema_type: Literal["Offer"] = Field(default="Offer", alias="@type")
    availability: Optional[str] = None
    price_currency: Optional[str] = Field(default="USD", alias="priceCurrency")
    price_specification: Optional[PriceSpecification] = Field(default=None, alias="priceSpecification")

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# SERVICE TYPES
# ============================================================================

class Audience(BaseModel):
    """
    Schema.org Audience
    https://schema.org/Audience
    """
    schema_type: Literal["Audience"] = Field(default="Audience", alias="@type")
    audience_type: str = Field(alias="audienceType")
    name: str

    model_config = ConfigDict(populate_by_name=True)


class Service(Thing):
    """
    Schema.org Service
    https://schema.org/Service
    """
    schema_type: Literal["Service"] = Field(default="Service", alias="@type")
    provider: Optional[Union[dict, "Organization"]] = None
    service_type: Optional[ServiceType] = Field(default=None, alias="serviceType")
    audience: Optional[Audience] = None
    offers: Optional[Offer] = None

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class OfferCatalog(BaseModel):
    """
    Schema.org OfferCatalog
    https://schema.org/OfferCatalog
    """
    schema_type: Literal["OfferCatalog"] = Field(default="OfferCatalog", alias="@type")
    schema_id: Optional[HttpUrl] = Field(default=None, alias="@id")
    name: str
    item_list_element: List[Union[dict, Service]] = Field(alias="itemListElement")

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# ORGANIZATION TYPES
# ============================================================================

class Organization(Thing):
    """
    Schema.org Organization
    https://schema.org/Organization
    """
    schema_type: Literal["Organization"] = Field(default="Organization", alias="@type")
    alternate_name: Optional[str] = Field(default=None, alias="alternateName")
    logo: Optional[Union[HttpUrl, ImageObject]] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    address: Optional[PostalAddress] = None
    area_served: Optional[Union[Country, dict]] = Field(default=None, alias="areaServed")
    founder: Optional[Person] = None
    knows_about: Optional[List[str]] = Field(default=None, alias="knowsAbout")
    has_offer_catalog: Optional[OfferCatalog] = Field(default=None, alias="hasOfferCatalog")
    founding_date: Optional[str] = Field(default=None, alias="foundingDate")
    slogan: Optional[str] = None
    same_as: Optional[List[HttpUrl]] = Field(default=None, alias="sameAs")
    contact_point: Optional[ContactPoint] = Field(default=None, alias="contactPoint")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class ProfessionalService(Thing):
    """
    Schema.org ProfessionalService
    https://schema.org/ProfessionalService
    """
    schema_type: Literal["ProfessionalService"] = Field(default="ProfessionalService", alias="@type")
    provider: Optional[Union[dict, Organization]] = None
    service_type: Optional[str] = Field(default=None, alias="serviceType")
    category: Optional[str] = None
    area_served: Optional[Union[Country, dict]] = Field(default=None, alias="areaServed")
    audience: Optional[Audience] = None
    has_offer_catalog: Optional[OfferCatalog] = Field(default=None, alias="hasOfferCatalog")

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# WEBSITE TYPES
# ============================================================================

class EntryPoint(BaseModel):
    """
    Schema.org EntryPoint
    https://schema.org/EntryPoint
    """
    schema_type: Literal["EntryPoint"] = Field(default="EntryPoint", alias="@type")
    url_template: str = Field(alias="urlTemplate")

    model_config = ConfigDict(populate_by_name=True)


class SearchAction(BaseModel):
    """
    Schema.org SearchAction
    https://schema.org/SearchAction
    """
    schema_type: Literal["SearchAction"] = Field(default="SearchAction", alias="@type")
    target: EntryPoint
    query_input: str = Field(alias="query-input")

    model_config = ConfigDict(populate_by_name=True)


class WebSite(Thing):
    """
    Schema.org WebSite
    https://schema.org/WebSite
    """
    schema_type: Literal["WebSite"] = Field(default="WebSite", alias="@type")
    publisher: Optional[Union[dict, Organization]] = None
    potential_action: Optional[SearchAction] = Field(default=None, alias="potentialAction")

    model_config = ConfigDict(populate_by_name=True)


class WebPage(Thing):
    """
    Schema.org WebPage
    https://schema.org/WebPage
    """
    schema_type: Literal["WebPage"] = Field(default="WebPage", alias="@type")
    is_part_of: Optional[Union[dict, WebSite]] = Field(default=None, alias="isPartOf")
    about: Optional[Union[dict, Organization]] = None
    breadcrumb: Optional[Union[dict, "BreadcrumbList"]] = None

    model_config = ConfigDict(populate_by_name=True)


class ListItem(BaseModel):
    """
    Schema.org ListItem
    https://schema.org/ListItem
    """
    schema_type: Literal["ListItem"] = Field(default="ListItem", alias="@type")
    position: int
    name: str
    item: Optional[HttpUrl] = None

    model_config = ConfigDict(populate_by_name=True)


class BreadcrumbList(BaseModel):
    """
    Schema.org BreadcrumbList
    https://schema.org/BreadcrumbList
    """
    schema_type: Literal["BreadcrumbList"] = Field(default="BreadcrumbList", alias="@type")
    schema_id: Optional[HttpUrl] = Field(default=None, alias="@id")
    item_list_element: List[ListItem] = Field(alias="itemListElement")

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# USER & DATABASE TYPES (from Prisma)
# ============================================================================

class User(BaseModel):
    """User model from Prisma schema"""
    id: UUID
    auth0_id: str
    email: str
    email_verified: bool = False
    name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    login_count: int = 0
    blocked: bool = False
    metadata: Optional[dict] = {}

    model_config = ConfigDict(use_enum_values=True)


class UserProfile(BaseModel):
    """User profile model from Prisma schema"""
    id: UUID
    user_id: Optional[UUID] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    locale: str = "en-US"
    preferences: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(use_enum_values=True)


class Role(BaseModel):
    """Role model from Prisma schema"""
    id: UUID
    name: str
    description: Optional[str] = None
    permissions: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(use_enum_values=True)


class UserRole(BaseModel):
    """User role assignment from Prisma schema"""
    id: UUID
    user_id: Optional[UUID] = None
    role_id: Optional[UUID] = None
    granted_at: Optional[datetime] = None
    granted_by: Optional[UUID] = None

    model_config = ConfigDict(use_enum_values=True)


class UserSession(BaseModel):
    """User session model from Prisma schema"""
    id: UUID
    user_id: Optional[UUID] = None
    session_token: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    created_at: Optional[datetime] = None
    expires_at: datetime
    last_activity: Optional[datetime] = None
    is_active: bool = True

    model_config = ConfigDict(use_enum_values=True)


class UserActivity(BaseModel):
    """User activity tracking from Prisma schema"""
    id: UUID
    user_id: Optional[UUID] = None
    activity_type: ActivityType
    description: Optional[str] = None
    metadata: Optional[dict] = {}
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(use_enum_values=True)


# ============================================================================
# INTEGRITY STUDIO SPECIFIC TYPES
# ============================================================================

class IntegrityStudioOrganization(Organization):
    """Complete Integrity Studio organization model"""
    schema_type: Literal["Organization"] = Field(default="Organization", alias="@type")
    name: str = "Integrity Studio"
    alternate_name: str = "The Integrity Studio"
    url: HttpUrl = Field(default="https://integritystudio.ai/")
    description: str = (
        "AI consultancy helping nonprofits leverage automation to increase funding, "
        "reduce costs, and amplify mission impact."
    )
    email: EmailStr = "hello@integritystudio.ai"
    telephone: str = "+1-512-829-1644"
    founding_date: str = "2024"
    slogan: str = "Empowering Nonprofits Through AI-Aware Compliance"

    # Services
    services: List[Service] = []


class IntegrityStudioService(Service):
    """Enhanced service model with pricing"""
    price: Optional[Decimal] = None
    price_description: Optional[str] = None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_integrity_studio_organization() -> IntegrityStudioOrganization:
    """
    Factory function to create complete Integrity Studio organization
    with all schema.org structured data
    """

    # Create address
    address = PostalAddress(
        addressLocality="Austin",
        addressRegion="TX",
        addressCountry="US"
    )

    # Create area served
    area_served = Country(name="United States")

    # Create founder
    founder = Person(
        schema_id="https://integritystudio.ai/#founder",
        schema_type="Person",
        name="Alyshia Ledlie",
        jobTitle="Founder & AI Consultant",
        url="https://calendly.com/alyshialedlie",
        email="hello@integritystudio.ai",
        worksFor={"@id": "https://integritystudio.ai/#organization"},
        knowsAbout=[
            "Artificial Intelligence",
            "Nonprofit Technology",
            "AI Compliance",
            "Automation",
            "Grant Writing",
            "Fundraising Technology"
        ]
    )

    # Create logo
    logo = ImageObject(
        url="https://integritystudio.ai/logo.png",
        width=512,
        height=512
    )

    # Create contact point
    contact_point = ContactPoint(
        telephone="+1-512-829-1644",
        email="hello@integritystudio.ai",
        contactType="Sales",
        areaServed="US",
        availableLanguage=["English"]
    )

    # Create services
    services = create_all_services()

    # Create offer catalog
    offer_catalog = OfferCatalog(
        schema_id="https://integritystudio.ai/#services",
        name="AI Solutions for Nonprofits",
        itemListElement=[{"@id": svc.schema_id} for svc in services if svc.schema_id]
    )

    # Create organization
    org = IntegrityStudioOrganization(
        schema_id="https://integritystudio.ai/#organization",
        logo=logo,
        image="https://integritystudio.ai/og-image.jpg",
        address=address,
        areaServed=area_served,
        founder=founder,
        knowsAbout=[
            "Artificial Intelligence",
            "Nonprofit Technology",
            "AI Consulting",
            "Compliance and Safety",
            "Automation",
            "Impact Measurement",
            "Grant Management",
            "Donor Engagement"
        ],
        hasOfferCatalog=offer_catalog,
        sameAs=[
            "https://calendly.com/alyshialedlie",
            "https://www.linkedin.com/company/integrity-studio",
            "https://twitter.com/integritystudio"
        ],
        contactPoint=contact_point,
        services=services
    )

    return org


def create_all_services() -> List[IntegrityStudioService]:
    """Create all service definitions"""

    nonprofit_audience = Audience(
        audienceType="Nonprofit Organizations",
        name="Mission-driven organizations and nonprofits"
    )

    services = [
        IntegrityStudioService(
            schema_id="https://integritystudio.ai/#service-ai-integration",
            schema_type="Service",
            name="AI Integration & Automation",
            description="Streamline operations with intelligent automation using Airtable, Zapier, and Google for Nonprofits. Automate donor acknowledgments, intake forms, and grant tracking.",
            provider={"@id": "https://integritystudio.ai/#organization"},
            serviceType=ServiceType.AI_INTEGRATION,
            audience=nonprofit_audience,
            price=Decimal("2500"),
            offers=Offer(
                availability="https://schema.org/InStock",
                priceCurrency="USD",
                priceSpecification=PriceSpecification(
                    priceCurrency="USD",
                    price="2500",
                    valueAddedTaxIncluded=False
                )
            )
        ),
        IntegrityStudioService(
            schema_id="https://integritystudio.ai/#service-compliance",
            schema_type="Service",
            name="Compliance & Safety",
            description="Ensure your AI implementations meet regulatory requirements and ethical standards. Build trust and safety layers early in your organization's digital transformation.",
            provider={"@id": "https://integritystudio.ai/#organization"},
            serviceType=ServiceType.COMPLIANCE,
            price=Decimal("3500"),
            offers=Offer(
                availability="https://schema.org/InStock",
                priceCurrency="USD",
                priceSpecification=PriceSpecification(
                    priceCurrency="USD",
                    price="3500",
                    valueAddedTaxIncluded=False
                )
            )
        ),
        IntegrityStudioService(
            schema_id="https://integritystudio.ai/#service-growth",
            schema_type="Service",
            name="Strategic Growth Planning",
            description="Develop sustainable funding strategies with AI-powered grant matching, donor engagement optimization, and performance tracking systems.",
            provider={"@id": "https://integritystudio.ai/#organization"},
            serviceType=ServiceType.STRATEGIC_PLANNING,
            price=Decimal("5000"),
            offers=Offer(
                availability="https://schema.org/InStock",
                priceCurrency="USD",
                priceSpecification=PriceSpecification(
                    priceCurrency="USD",
                    price="5000",
                    valueAddedTaxIncluded=False
                )
            )
        ),
        IntegrityStudioService(
            schema_id="https://integritystudio.ai/#service-impact",
            schema_type="Service",
            name="Impact Measurement",
            description="Create comprehensive dashboards and reporting systems to track your organization's impact, measure AI ROI, and demonstrate value to stakeholders.",
            provider={"@id": "https://integritystudio.ai/#organization"},
            serviceType=ServiceType.ANALYTICS_REPORTING,
            price=Decimal("2000"),
            offers=Offer(
                availability="https://schema.org/InStock",
                priceCurrency="USD",
                priceSpecification=PriceSpecification(
                    priceCurrency="USD",
                    price="2000",
                    valueAddedTaxIncluded=False
                )
            )
        ),
        IntegrityStudioService(
            schema_id="https://integritystudio.ai/#service-training",
            schema_type="Service",
            name="Team Training & Support",
            description="Empower your team with AI literacy training, best practices workshops, and ongoing support to maximize your technology investments.",
            provider={"@id": "https://integritystudio.ai/#organization"},
            serviceType=ServiceType.TRAINING_EDUCATION,
            price=Decimal("1500"),
            offers=Offer(
                availability="https://schema.org/InStock",
                priceCurrency="USD",
                priceSpecification=PriceSpecification(
                    priceCurrency="USD",
                    price="1500",
                    valueAddedTaxIncluded=False
                )
            )
        ),
        IntegrityStudioService(
            schema_id="https://integritystudio.ai/#service-custom",
            schema_type="Service",
            name="Custom Solutions",
            description="Tailored AI solutions designed specifically for your organization's unique needs, mission, and operational requirements.",
            provider={"@id": "https://integritystudio.ai/#organization"},
            serviceType=ServiceType.CUSTOM_DEVELOPMENT,
            price_description="Custom pricing based on project scope",
            offers=Offer(
                availability="https://schema.org/InStock",
                priceCurrency="USD",
                priceSpecification=PriceSpecification(
                    priceCurrency="USD",
                    description="Custom pricing based on project scope"
                )
            )
        )
    ]

    return services


def export_to_json_ld(obj: BaseModel) -> dict:
    """
    Export a Pydantic model to JSON-LD format for schema.org
    """
    return obj.model_dump(by_alias=True, exclude_none=True)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import json

    # Create the organization
    org = create_integrity_studio_organization()

    # Export to JSON-LD
    json_ld = export_to_json_ld(org)

    # Pretty print (first 2000 chars)
    output = json.dumps(json_ld, indent=2, default=str)
    print(output[:2000] + "...")
