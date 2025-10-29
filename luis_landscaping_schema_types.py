"""
Luis Landscaping & Handyman Services - Schema.org Compatible Type Definitions with Pydantic Models

This module defines structured data types for Luis Landscaping & Handyman Services
that are compatible with both Schema.org vocabulary and Pydantic validation.

Based on analysis of: ~/code/IntegrityStudioClients/luis-landscaping
"""

from typing import Optional, List, Literal, Union
from datetime import datetime, time
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict
from enum import Enum

# EmailStr requires email-validator package
# For simplicity, we'll use str for email addresses
# To enable email validation, install: pip install 'pydantic[email]'
EmailStr = str


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ServiceType(str, Enum):
    """Types of services offered"""
    TREE_SERVICE = "Tree Service"
    LANDSCAPING = "Landscaping"
    LAWN_MAINTENANCE = "Lawn Maintenance"
    HANDYMAN_SERVICES = "Handyman Services"
    GARDEN_SERVICES = "Garden Services"


class DayOfWeek(str, Enum):
    """Schema.org DayOfWeek enumeration"""
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class ContactType(str, Enum):
    """Contact form message types"""
    GENERAL_INQUIRY = "General Inquiry"
    SERVICE_REQUEST = "Service Request"
    QUOTE_REQUEST = "Quote Request"
    FEEDBACK = "Feedback"


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
# PLACE TYPES
# ============================================================================

class PostalAddress(BaseModel):
    """
    Schema.org PostalAddress
    https://schema.org/PostalAddress
    """
    schema_type: Literal["PostalAddress"] = Field(default="PostalAddress", alias="@type")
    street_address: str = Field(alias="streetAddress")
    address_locality: str = Field(alias="addressLocality")
    address_region: str = Field(alias="addressRegion")
    postal_code: str = Field(alias="postalCode")
    address_country: str = Field(default="US", alias="addressCountry")

    model_config = ConfigDict(populate_by_name=True)


class GeoCoordinates(BaseModel):
    """
    Schema.org GeoCoordinates
    https://schema.org/GeoCoordinates
    """
    schema_type: Literal["GeoCoordinates"] = Field(default="GeoCoordinates", alias="@type")
    latitude: float
    longitude: float

    model_config = ConfigDict(populate_by_name=True)


class Place(Thing):
    """
    Schema.org Place
    https://schema.org/Place
    """
    schema_type: Literal["Place"] = Field(default="Place", alias="@type")
    address: Optional[PostalAddress] = None
    geo: Optional[GeoCoordinates] = None
    telephone: Optional[str] = None


# ============================================================================
# TIME-RELATED TYPES
# ============================================================================

class OpeningHoursSpecification(BaseModel):
    """
    Schema.org OpeningHoursSpecification
    https://schema.org/OpeningHoursSpecification
    """
    schema_type: Literal["OpeningHoursSpecification"] = Field(
        default="OpeningHoursSpecification",
        alias="@type"
    )
    day_of_week: Union[DayOfWeek, List[DayOfWeek]] = Field(alias="dayOfWeek")
    opens: str  # Time in HH:MM format
    closes: str  # Time in HH:MM format

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    @field_validator('opens', 'closes')
    @classmethod
    def validate_time_format(cls, v):
        """Validate HH:MM time format"""
        try:
            time.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError(f"Time must be in HH:MM format, got: {v}")


# ============================================================================
# SERVICE & OFFER TYPES
# ============================================================================

class Service(Thing):
    """
    Schema.org Service
    https://schema.org/Service
    """
    schema_type: Literal["Service"] = Field(default="Service", alias="@type")
    provider: Optional[Union[dict, "LocalBusiness"]] = None
    service_type: Optional[ServiceType] = Field(default=None, alias="serviceType")
    area_served: Optional[Union[Place, dict]] = Field(default=None, alias="areaServed")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class Offer(BaseModel):
    """
    Schema.org Offer
    https://schema.org/Offer
    """
    schema_type: Literal["Offer"] = Field(default="Offer", alias="@type")
    item_offered: Union[Service, dict] = Field(alias="itemOffered")
    price_currency: str = Field(default="USD", alias="priceCurrency")
    availability: str = Field(default="https://schema.org/InStock")

    model_config = ConfigDict(populate_by_name=True)


class OfferCatalog(BaseModel):
    """
    Schema.org OfferCatalog
    https://schema.org/OfferCatalog
    """
    schema_type: Literal["OfferCatalog"] = Field(default="OfferCatalog", alias="@type")
    name: str
    item_list_element: List[Offer] = Field(alias="itemListElement")

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# ORGANIZATION TYPES
# ============================================================================

class ContactPoint(BaseModel):
    """
    Schema.org ContactPoint
    https://schema.org/ContactPoint
    """
    schema_type: Literal["ContactPoint"] = Field(default="ContactPoint", alias="@type")
    telephone: str
    contact_type: str = Field(alias="contactType")
    available_language: Optional[List[str]] = Field(default=None, alias="availableLanguage")

    model_config = ConfigDict(populate_by_name=True)


class Organization(Thing):
    """
    Schema.org Organization
    https://schema.org/Organization
    """
    schema_type: Literal["Organization"] = Field(default="Organization", alias="@type")
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[PostalAddress] = None


class LocalBusiness(Organization):
    """
    Schema.org LocalBusiness
    https://schema.org/LocalBusiness
    """
    schema_type: Literal["LocalBusiness"] = Field(default="LocalBusiness", alias="@type")
    opening_hours_specification: Optional[List[OpeningHoursSpecification]] = Field(
        default=None,
        alias="openingHoursSpecification"
    )
    geo: Optional[GeoCoordinates] = None
    price_range: Optional[str] = Field(default=None, alias="priceRange")
    area_served: Optional[Union[str, List[str], dict]] = Field(default=None, alias="areaServed")
    has_offer_catalog: Optional[OfferCatalog] = Field(default=None, alias="hasOfferCatalog")
    contact_point: Optional[ContactPoint] = Field(default=None, alias="contactPoint")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


# ============================================================================
# CONTACT FORM TYPES
# ============================================================================

class ContactFormData(BaseModel):
    """Contact form submission data"""
    name: str
    email: EmailStr
    phone: str
    message: str
    contact_type: ContactType = ContactType.GENERAL_INQUIRY
    submitted_at: Optional[datetime] = None

    model_config = ConfigDict(use_enum_values=True)

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Basic phone validation"""
        # Remove common separators
        cleaned = v.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if not cleaned.isdigit() or len(cleaned) < 10:
            raise ValueError(f"Invalid phone number: {v}")
        return v


class ValidationError(BaseModel):
    """Form validation error"""
    field: str
    message: str


# ============================================================================
# LUIS LANDSCAPING SPECIFIC TYPES
# ============================================================================

class LuisLandscapingBusiness(LocalBusiness):
    """Complete Luis Landscaping & Handyman Services business model"""
    schema_type: Literal["LocalBusiness"] = Field(default="LocalBusiness", alias="@type")
    name: str = "Luis Landscaping & Handyman Services"
    description: str = (
        "Professional tree service, landscaping, lawn maintenance, handyman services, "
        "and garden services in Austin, TX"
    )
    telephone: str = "(737) 420-7339"

    # Services offered
    services: List[Service] = []


class LuisLandscapingService(Service):
    """Enhanced service model for Luis Landscaping"""
    service_category: Optional[str] = Field(default=None, alias="serviceCategory")
    typical_duration: Optional[str] = None  # e.g., "1-2 hours", "Full day"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_luis_landscaping_business() -> LuisLandscapingBusiness:
    """
    Factory function to create complete Luis Landscaping business
    with all schema.org structured data
    """

    # Create address
    address = PostalAddress(
        streetAddress="12028 Timber Heights Drive",
        addressLocality="Austin",
        addressRegion="TX",
        postalCode="78754",
        addressCountry="US"
    )

    # Create geo coordinates (Austin, TX - approximate)
    geo = GeoCoordinates(
        latitude=30.3672,
        longitude=-97.6431
    )

    # Create opening hours (typical landscaping business hours)
    opening_hours = [
        OpeningHoursSpecification(
            dayOfWeek=[
                DayOfWeek.MONDAY,
                DayOfWeek.TUESDAY,
                DayOfWeek.WEDNESDAY,
                DayOfWeek.THURSDAY,
                DayOfWeek.FRIDAY
            ],
            opens="07:00",
            closes="18:00"
        ),
        OpeningHoursSpecification(
            dayOfWeek=DayOfWeek.SATURDAY,
            opens="08:00",
            closes="15:00"
        )
    ]

    # Create contact point
    contact_point = ContactPoint(
        telephone="(737) 420-7339",
        contactType="Customer Service",
        availableLanguage=["English", "Spanish"]
    )

    # Create services
    services = create_all_services()

    # Create offer catalog
    offers = [
        Offer(
            itemOffered={"@id": svc.schema_id} if svc.schema_id else svc,
            priceCurrency="USD",
            availability="https://schema.org/InStock"
        )
        for svc in services
    ]

    offer_catalog = OfferCatalog(
        name="Landscaping & Handyman Services",
        itemListElement=offers
    )

    # Create business
    business = LuisLandscapingBusiness(
        schema_id="https://luislandscaping.com/#business",
        address=address,
        geo=geo,
        openingHoursSpecification=opening_hours,
        priceRange="$$",
        areaServed=["Austin, TX", "Round Rock, TX", "Cedar Park, TX", "Pflugerville, TX"],
        contactPoint=contact_point,
        hasOfferCatalog=offer_catalog,
        services=services
    )

    return business


def create_all_services() -> List[LuisLandscapingService]:
    """Create all service definitions"""

    services = [
        LuisLandscapingService(
            schema_id="https://luislandscaping.com/#service-tree",
            schema_type="Service",
            name="Tree Service",
            description="Professional tree trimming, pruning, and removal services. Keeping your trees healthy and your property safe.",
            provider={"@id": "https://luislandscaping.com/#business"},
            serviceType=ServiceType.TREE_SERVICE,
            serviceCategory="Outdoor Maintenance",
            areaServed={"@type": "City", "name": "Austin, TX"}
        ),
        LuisLandscapingService(
            schema_id="https://luislandscaping.com/#service-landscaping",
            schema_type="Service",
            name="Landscaping",
            description="Complete landscaping design and installation. Transform your outdoor space with beautiful, sustainable landscapes.",
            provider={"@id": "https://luislandscaping.com/#business"},
            serviceType=ServiceType.LANDSCAPING,
            serviceCategory="Landscape Design",
            areaServed={"@type": "City", "name": "Austin, TX"}
        ),
        LuisLandscapingService(
            schema_id="https://luislandscaping.com/#service-lawn",
            schema_type="Service",
            name="Lawn Maintenance",
            description="Regular lawn mowing, edging, trimming, and maintenance to keep your lawn looking pristine all year round.",
            provider={"@id": "https://luislandscaping.com/#business"},
            serviceType=ServiceType.LAWN_MAINTENANCE,
            serviceCategory="Outdoor Maintenance",
            typicalDuration="1-2 hours",
            areaServed={"@type": "City", "name": "Austin, TX"}
        ),
        LuisLandscapingService(
            schema_id="https://luislandscaping.com/#service-handyman",
            schema_type="Service",
            name="Handyman Services",
            description="General handyman services for home repairs, installations, and maintenance tasks.",
            provider={"@id": "https://luislandscaping.com/#business"},
            serviceType=ServiceType.HANDYMAN_SERVICES,
            serviceCategory="Home Maintenance",
            areaServed={"@type": "City", "name": "Austin, TX"}
        ),
        LuisLandscapingService(
            schema_id="https://luislandscaping.com/#service-garden",
            schema_type="Service",
            name="Garden Services",
            description="Professional garden design, planting, weeding, and maintenance to create beautiful outdoor living spaces.",
            provider={"@id": "https://luislandscaping.com/#business"},
            serviceType=ServiceType.GARDEN_SERVICES,
            serviceCategory="Garden Care",
            areaServed={"@type": "City", "name": "Austin, TX"}
        )
    ]

    return services


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
    publisher: Optional[dict] = None
    potential_action: Optional[SearchAction] = Field(default=None, alias="potentialAction")

    model_config = ConfigDict(populate_by_name=True)


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

    # Create the business
    business = create_luis_landscaping_business()

    # Export to JSON-LD
    json_ld = export_to_json_ld(business)

    # Pretty print (first 2000 chars)
    output = json.dumps(json_ld, indent=2, default=str)
    print(output[:2000] + "...")
