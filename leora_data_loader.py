"""
Leora Home Health - Data Loader Utilities

This module provides utilities to load data from the Leora codebase
and convert it into structured Pydantic models with schema.org compatibility.
"""

import csv
from pathlib import Path
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from leora_schema_types import (
    ProductVariant,
    ServiceCategory,
    ProductTier,
    PricingDuration,
    TaxClass,
    LeoraHomeHealth,
    create_leora_organization
)


class LeoraDataLoader:
    """Loads and parses Leora data from CSV files"""

    def __init__(self, base_path: str = "~/code/IntegrityStudioClients/Leora"):
        """
        Initialize the data loader

        Args:
            base_path: Path to the Leora codebase root directory
        """
        self.base_path = Path(base_path).expanduser()

    def _parse_price(self, price_str: str) -> Optional[Decimal]:
        """
        Parse price string like '$2,999.00' to Decimal

        Args:
            price_str: Price string with currency symbol and commas

        Returns:
            Decimal representation or None if empty
        """
        if not price_str or price_str.strip() == "":
            return None

        # Remove currency symbol, commas, and whitespace
        cleaned = price_str.replace('$', '').replace(',', '').strip()

        try:
            return Decimal(cleaned)
        except Exception:
            return None

    def _parse_datetime(self, date_str: str) -> Optional[datetime]:
        """
        Parse datetime string from CSV

        Args:
            date_str: Date string in format like 'Tue Oct 31 2023 14:00:20 GMT+0000...'

        Returns:
            datetime object or None if parsing fails
        """
        if not date_str or date_str.strip() == "":
            return None

        try:
            # Try parsing the format used in the CSV
            # Example: "Tue Oct 31 2023 14:00:20 GMT+0000 (Coordinated Universal Time)"
            parts = date_str.split(' GMT')[0]
            dt = datetime.strptime(parts, "%a %b %d %Y %H:%M:%S")
            return dt
        except Exception:
            return None

    def load_products(self) -> List[ProductVariant]:
        """
        Load product variants from CSV file

        Returns:
            List of ProductVariant objects
        """
        products_file = self.base_path / "Leora Home Health - Products.csv"

        if not products_file.exists():
            raise FileNotFoundError(f"Products file not found: {products_file}")

        products = []

        with open(products_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    # Parse tier
                    tier_name = row['Product Name'].strip()
                    tier = ProductTier[tier_name.upper()]

                    # Parse duration
                    duration_value = row['Option1 Value'].strip()
                    duration = PricingDuration[duration_value.upper()]

                    # Create product variant
                    product = ProductVariant(
                        variant_id=row['Variant ID'],
                        product_id=row['Product ID'],
                        product_handle=row['Product Handle'],
                        product_name=row['Product Name'],
                        product_type=row['Product Type'],
                        product_description=row['Product Description'] or None,
                        product_categories=row['Product Categories'] or None,
                        tier=tier,
                        duration=duration,
                        price=self._parse_price(row['Variant Price']),
                        compare_at_price=self._parse_price(row['Variant Compare-at Price']),
                        tax_class=TaxClass.STANDARD_TAXABLE,
                        requires_shipping=row['Requires Shipping'].lower() == 'true',
                        main_variant_image=row['Main Variant Image'] or None,
                        created_on=self._parse_datetime(row['Created On']),
                        updated_on=self._parse_datetime(row['Updated On']),
                        published_on=self._parse_datetime(row['Published On'])
                    )

                    products.append(product)

                except Exception as e:
                    print(f"Warning: Failed to parse product row: {e}")
                    continue

        return products

    def load_categories(self) -> List[ServiceCategory]:
        """
        Load service categories from CSV file

        Returns:
            List of ServiceCategory objects
        """
        categories_file = self.base_path / "Leora Home Health - Categories.csv"

        if not categories_file.exists():
            raise FileNotFoundError(f"Categories file not found: {categories_file}")

        categories = []

        with open(categories_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    category = ServiceCategory(
                        name=row['Name'],
                        slug=row['Category - Link'],
                        description=row['Category - Description'] or None,
                        collection_id=row['Collection ID'],
                        item_id=row['Item ID'],
                        archived=row['Archived'].lower() == 'true',
                        draft=row['Draft'].lower() == 'true',
                        created_on=self._parse_datetime(row['Created On']),
                        updated_on=self._parse_datetime(row['Updated On']),
                        published_on=self._parse_datetime(row['Published On'])
                    )

                    categories.append(category)

                except Exception as e:
                    print(f"Warning: Failed to parse category row: {e}")
                    continue

        return categories

    def create_complete_organization(self) -> LeoraHomeHealth:
        """
        Create a complete LeoraHomeHealth organization with all data loaded

        Returns:
            LeoraHomeHealth object with products and categories populated
        """
        # Create base organization
        org = create_leora_organization()

        # Load and attach products
        try:
            org.products = self.load_products()
            print(f"Loaded {len(org.products)} product variants")
        except Exception as e:
            print(f"Warning: Could not load products: {e}")
            org.products = []

        # Load and attach categories
        try:
            org.categories = self.load_categories()
            print(f"Loaded {len(org.categories)} categories")
        except Exception as e:
            print(f"Warning: Could not load categories: {e}")
            org.categories = []

        return org


def generate_product_json_ld(product: ProductVariant) -> dict:
    """
    Generate schema.org JSON-LD for a product variant

    Args:
        product: ProductVariant object

    Returns:
        Dictionary representing JSON-LD
    """
    from leora_schema_types import Product, Offer, export_to_json_ld

    # Create Product
    prod = Product(
        schema_type="Product",
        schema_id=f"https://www.leorahomehealth.com/#product-{product.product_handle}",
        name=f"{product.product_name} - {product.duration}",
        description=product.product_description,
        sku=product.variant_id,
        category=product.product_categories,
        image=product.main_variant_image,
        brand="Leora Home Health"
    )

    # Create Offer
    offer = Offer(
        itemOffered=prod,
        price=product.price,
        priceCurrency="USD"
    )

    # Export without offers first to avoid circular reference
    product_dict = export_to_json_ld(prod)

    # Add offer separately
    product_dict["offers"] = [export_to_json_ld(offer)]

    return product_dict


def export_all_to_json_ld(org: LeoraHomeHealth, output_file: Optional[str] = None) -> dict:
    """
    Export complete organization to JSON-LD format

    Args:
        org: LeoraHomeHealth organization
        output_file: Optional file path to save JSON-LD

    Returns:
        Dictionary representing JSON-LD
    """
    import json
    from leora_schema_types import export_to_json_ld

    json_ld = export_to_json_ld(org)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_ld, f, indent=2, default=str)
        print(f"JSON-LD exported to: {output_file}")

    return json_ld


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import json

    # Initialize loader
    loader = LeoraDataLoader()

    # Load products
    print("\n=== Loading Products ===")
    products = loader.load_products()
    print(f"Found {len(products)} product variants")

    for product in products[:3]:  # Show first 3
        print(f"\nProduct: {product.product_name} ({product.duration})")
        print(f"  Price: ${product.price}")
        print(f"  Compare Price: ${product.compare_at_price}")
        print(f"  Tier: {product.tier}")

    # Load categories
    print("\n\n=== Loading Categories ===")
    categories = loader.load_categories()
    print(f"Found {len(categories)} categories")

    for category in categories:
        print(f"\nCategory: {category.name}")
        print(f"  Slug: {category.slug}")
        print(f"  Description: {category.description[:50]}..." if category.description else "  No description")

    # Create complete organization
    print("\n\n=== Creating Complete Organization ===")
    org = loader.create_complete_organization()

    # Export to JSON-LD
    print("\n\n=== Exporting to JSON-LD ===")
    json_ld = export_all_to_json_ld(org, "leora_complete.json")

    # Show a sample
    print("\nSample JSON-LD structure:")
    print(json.dumps(json_ld, indent=2, default=str)[:1000] + "...")

    # Generate individual product JSON-LD
    if products:
        print("\n\n=== Sample Product JSON-LD ===")
        product_json_ld = generate_product_json_ld(products[0])
        print(json.dumps(product_json_ld, indent=2, default=str))
