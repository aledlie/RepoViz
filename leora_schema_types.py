"""
Leora Home Health - Schema.org Compatible Type Definitions with Pydantic Models

This module defines structured data types for the Leora Home Health application
that are compatible with both Schema.org vocabulary and Pydantic validation.

Based on analysis of: ~/code/IntegrityStudioClients/Leora
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

class DayOfWeek(str, Enum):
    """Schema.org DayOfWeek enumeration"""
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class ServiceType(str, Enum):
    """Types of home health services offered"""
    SKILLED_NURSING = "Skilled Nursing"
    HOME_HEALTH_AIDE = "Home Health Aide (HHA)"
    PERSONAL_ASSISTANT = "Personal Assistant Services (PAS)"
    MEDICAL_SOCIAL_SERVICES = "Medical Social Services"


class ProductTier(str, Enum):
    """Product/Service tier levels"""
    BASIC = "Basic"
    STANDARD = "Standard"
    LUXURY = "Luxury"


class PricingDuration(str, Enum):
    """Pricing duration options"""
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


class TaxClass(str, Enum):
    """Tax classification for products"""
    STANDARD_TAXABLE = "standard-taxable"


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
    street_address: Optional[str] = Field(default=None, alias="streetAddress")
    address_locality: str = Field(alias="addressLocality")
    address_region: str = Field(alias="addressRegion")
    postal_code: Optional[str] = Field(default=None, alias="postalCode")
    address_country: str = Field(alias="addressCountry")

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


class City(Place):
    """
    Schema.org City
    https://schema.org/City
    """
    schema_type: Literal["City"] = Field(default="City", alias="@type")
    contained_in: Optional["State"] = Field(default=None, alias="containedIn")

    model_config = ConfigDict(populate_by_name=True)


class State(Place):
    """
    Schema.org State
    https://schema.org/State
    """
    schema_type: Literal["State"] = Field(default="State", alias="@type")


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
# SERVICE TYPES
# ============================================================================

class Service(Thing):
    """
    Schema.org Service
    https://schema.org/Service
    """
    schema_type: Literal["Service"] = Field(default="Service", alias="@type")
    provider: Optional[Union[dict, "Organization"]] = None
    area_served: Optional[Union[Place, City, State, List[Union[Place, City, State]]]] = Field(
        default=None,
        alias="areaServed"
    )
    service_type: Optional[ServiceType] = Field(default=None, alias="serviceType")

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


# ============================================================================
# OFFER & PRODUCT TYPES
# ============================================================================

class MonetaryAmount(BaseModel):
    """
    Schema.org MonetaryAmount
    https://schema.org/MonetaryAmount
    """
    schema_type: Literal["MonetaryAmount"] = Field(default="MonetaryAmount", alias="@type")
    currency: str = "USD"
    value: Decimal

    model_config = ConfigDict(populate_by_name=True)


class Offer(BaseModel):
    """
    Schema.org Offer
    https://schema.org/Offer
    """
    schema_type: Literal["Offer"] = Field(default="Offer", alias="@type")
    item_offered: Union[Service, "Product"] = Field(alias="itemOffered")
    price: Optional[Decimal] = None
    price_currency: Optional[str] = Field(default="USD", alias="priceCurrency")
    availability: Optional[str] = None
    valid_from: Optional[datetime] = Field(default=None, alias="validFrom")

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


class Product(Thing):
    """
    Schema.org Product
    https://schema.org/Product
    """
    schema_type: Literal["Product"] = Field(default="Product", alias="@type")
    sku: Optional[str] = None
    category: Optional[str] = None
    offers: Optional[List[Offer]] = None
    brand: Optional[Union[str, "Organization"]] = None

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
    logo: Optional[HttpUrl] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[PostalAddress] = None
    same_as: Optional[List[HttpUrl]] = Field(default=None, alias="sameAs")

    model_config = ConfigDict(populate_by_name=True)


class LocalBusiness(Organization):
    """
    Schema.org LocalBusiness
    https://schema.org/LocalBusiness
    """
    schema_type: Literal["LocalBusiness"] = Field(default="LocalBusiness", alias="@type")
    price_range: Optional[str] = Field(default=None, alias="priceRange")
    geo: Optional[GeoCoordinates] = None
    area_served: Optional[List[Union[City, State]]] = Field(default=None, alias="areaServed")
    opening_hours_specification: Optional[List[OpeningHoursSpecification]] = Field(
        default=None,
        alias="openingHoursSpecification"
    )
    has_offer_catalog: Optional[OfferCatalog] = Field(default=None, alias="hasOfferCatalog")

    model_config = ConfigDict(populate_by_name=True)


# ============================================================================
# LEORA-SPECIFIC DOMAIN MODELS
# ============================================================================

class ProductVariant(BaseModel):
    """Leora product variant with pricing options"""
    variant_id: str
    product_id: str
    product_handle: str
    product_name: str
    product_type: str
    product_description: Optional[str] = None
    product_categories: Optional[str] = None
    tier: ProductTier
    duration: PricingDuration
    price: Decimal
    compare_at_price: Optional[Decimal] = None
    tax_class: TaxClass = TaxClass.STANDARD_TAXABLE
    requires_shipping: bool = False
    main_variant_image: Optional[HttpUrl] = None
    more_variant_images: Optional[List[HttpUrl]] = None
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    published_on: Optional[datetime] = None

    model_config = ConfigDict(use_enum_values=True)


class ServiceCategory(BaseModel):
    """Service category definition"""
    name: str
    slug: str
    description: Optional[str] = None
    collection_id: str
    item_id: str
    archived: bool = False
    draft: bool = False
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    published_on: Optional[datetime] = None


class ContactInformation(BaseModel):
    """Contact information for the organization"""
    email: EmailStr
    phone: str
    facebook_url: Optional[HttpUrl] = None
    twitter_url: Optional[HttpUrl] = None
    instagram_url: Optional[HttpUrl] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Basic phone validation"""
        # Remove common separators
        cleaned = v.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if not cleaned.isdigit() or len(cleaned) < 10:
            raise ValueError(f"Invalid phone number: {v}")
        return v


class LeoraHomeHealth(LocalBusiness):
    """
    Complete schema.org representation of Leora Home Health organization
    """
    schema_type: Literal["LocalBusiness"] = Field(default="LocalBusiness", alias="@type")
    name: str = "Leora Home Health"
    url: HttpUrl = Field(default="https://www.leorahomehealth.com")
    description: str = (
        "Compassionate in-home health care services in Central Texas, "
        "offering Personal Assistant Services (PAS), Home Health Aide (HHA), "
        "and skilled nursing care."
    )
    telephone: str = "+1-512-222-8103"
    email: EmailStr = "appointments@leorahomehealth.com"
    price_range: str = "$$"

    # Services offered
    services: List[Service] = []

    # Product catalog
    products: List[ProductVariant] = []

    # Service categories
    categories: List[ServiceCategory] = []


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_leora_organization() -> LeoraHomeHealth:
    """
    Factory function to create a complete Leora Home Health organization
    with all schema.org structured data
    """

    # Create address
    address = PostalAddress(
        addressLocality="Austin",
        addressRegion="TX",
        addressCountry="US"
    )

    # Create geo coordinates
    geo = GeoCoordinates(
        latitude=30.2672,
        longitude=-97.7431
    )

    # Create area served
    austin = City(
        name="Austin",
        containedIn=State(name="Texas")
    )
    texas = State(name="Texas")

    # Create opening hours
    opening_hours = [
        OpeningHoursSpecification(
            dayOfWeek=[
                DayOfWeek.MONDAY,
                DayOfWeek.TUESDAY,
                DayOfWeek.WEDNESDAY,
                DayOfWeek.THURSDAY,
                DayOfWeek.FRIDAY
            ],
            opens="08:00",
            closes="17:00"
        )
    ]

    # Create services
    skilled_nursing = Service(
        schema_id="https://www.leorahomehealth.com/#skilled-nursing",
        name="Skilled Nursing",
        description="Professional nursing care delivered in the comfort of your home by licensed nurses.",
        provider={"@id": "https://www.leorahomehealth.com/#organization"},
        areaServed=texas,
        serviceType=ServiceType.SKILLED_NURSING
    )

    hha_service = Service(
        schema_id="https://www.leorahomehealth.com/#home-health-aide",
        name="Home Health Aide (HHA)",
        description="Certified home health aides providing personal care and assistance with daily activities.",
        provider={"@id": "https://www.leorahomehealth.com/#organization"},
        areaServed=texas,
        serviceType=ServiceType.HOME_HEALTH_AIDE
    )

    pas_service = Service(
        schema_id="https://www.leorahomehealth.com/#personal-assistant",
        name="Personal Assistant Services (PAS)",
        description="Professional caregivers assist with routine home activities (ADLs) while offering genuine companionship.",
        provider={"@id": "https://www.leorahomehealth.com/#organization"},
        areaServed=texas,
        serviceType=ServiceType.PERSONAL_ASSISTANT
    )

    mss_service = Service(
        schema_id="https://www.leorahomehealth.com/#medical-social-services",
        name="Medical Social Services",
        description="Professional social work services to support patients and families.",
        provider={"@id": "https://www.leorahomehealth.com/#organization"},
        areaServed=texas,
        serviceType=ServiceType.MEDICAL_SOCIAL_SERVICES
    )

    # Create offers
    offers = [
        Offer(itemOffered=skilled_nursing),
        Offer(itemOffered=hha_service),
        Offer(itemOffered=pas_service),
        Offer(itemOffered=mss_service)
    ]

    # Create offer catalog
    offer_catalog = OfferCatalog(
        name="Home Health Services",
        itemListElement=offers
    )

    # Create organization
    org = LeoraHomeHealth(
        schema_id="https://www.leorahomehealth.com/#organization",
        logo="https://cdn.prod.website-files.com/6700b1003622e22dbd310d9f/670f45bf03cdb5f2ed97b8f2_LHH-Logo.svg",
        image="https://cdn.prod.website-files.com/6700b1003622e22dbd310d9f/67a7bfffbb22352384ed25b4_LHH-OG-Home.jpg",
        address=address,
        geo=geo,
        areaServed=[austin, texas],
        openingHoursSpecification=opening_hours,
        sameAs=[
            "https://facebook.com/leorahomehealth",
            "https://twitter.com/leoarhomehealth",
            "https://instagram.com/leorahomehealth"
        ],
        hasOfferCatalog=offer_catalog,
        services=[skilled_nursing, hha_service, pas_service, mss_service]
    )

    return org


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
    leora = create_leora_organization()

    # Export to JSON-LD
    json_ld = export_to_json_ld(leora)

    # Pretty print
    print(json.dumps(json_ld, indent=2, default=str))
