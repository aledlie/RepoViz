# RepoViz

## Overview

This directory contains 14 code file(s) with extracted schemas.

**Git Remote:** git@github.com:aledlie/RepoViz.git

## Subdirectories

- `Generated Data/`
- `examples/`
- `git_commit_visualization_utilities.egg-info/`
- `logs/`
- `reports/`
- `tests/`

## Files and Schemas

### `analyze_integrity_studio.py` (python)

**Functions:**
- `get_file_language(file_path)` - Line 13
- `analyze_directory(base_path)` - Line 35
- `format_size(bytes_size)` - Line 97
- `main()` - Line 109

**Key Imports:** `collections`, `json`, `os`, `pathlib`

### `database_schema.py` (python)

**Classes:**
- `Repository` (extends: Base) - Line 23
  - Repository information table.
  - Methods: __repr__
- `Commit` (extends: Base) - Line 45
  - Individual commit data table.
  - Methods: __repr__
- `CommitSummary` (extends: Base) - Line 82
  - Aggregated commit statistics table.
  - Methods: __repr__
- `Chart` (extends: Base) - Line 113
  - Generated chart metadata table.
  - Methods: __repr__, get_configuration, set_configuration, get_schema_org_data, set_schema_org_data
- `DataFile` (extends: Base) - Line 169
  - Data file metadata table.
  - Methods: __repr__
- `DatabaseManager` - Line 199
  - Database management utilities.
  - Methods: __init__, create_tables, get_session, get_or_create_repository, add_commit (+3 more)

**Functions:**
- `initialize_database(database_url) -> DatabaseManager` - Line 425
- `import_commit_data_from_files(db_manager, repo_name) -> <ast.Constant object at 0x103ebc590>` - Line 432

**Key Imports:** `datetime`, `json`, `os`, `schemas`, `sqlalchemy` (+4 more)

### `enhanced_mcp_server.py` (python)

**Functions:**
- `get_repository_name() -> Optional[...]` - Line 46
- `run_data_collection_script(script_name) -> bool` - Line 62
- `list_tools() -> List[...]` - Line 139

**Key Imports:** `asyncio`, `enhanced_plot_scripts`, `json`, `mcp.server`, `mcp.server.models` (+8 more)

### `enhanced_plot_scripts.py` (python)

**Classes:**
- `EnhancedPlotter` - Line 30
  - Enhanced plotter with Pydantic configuration support.
  - Methods: __init__, load_commit_data, create_hour_bar_chart, create_day_pie_chart, create_month_pie_chart (+3 more)

**Functions:**
- `create_chart_from_config(config) -> str` - Line 355
- `create_chart_from_env() -> str` - Line 371
- `main()` - Line 412

**Key Imports:** `argparse`, `json`, `matplotlib.pyplot`, `numpy`, `os` (+4 more)

### `extract_schema_org.py` (python)

**Functions:**
- `fetch_webpage(url) -> str` - Line 15
- `extract_jsonld_scripts(html) -> List[...]` - Line 30
- `extract_meta_tags(html) -> Dict[...]` - Line 47
- `analyze_schema_org_data(url) -> Dict[...]` - Line 69
- `main()` - Line 106

**Key Imports:** `datetime`, `json`, `re`, `sys`, `typing` (+2 more)

### `integrity_studio_data_loader.py` (python)

**Classes:**
- `IntegrityStudioDataLoader` - Line 29
  - Loads and manages Integrity Studio data
  - Methods: __init__, load_schema_from_html, create_sample_users, create_sample_roles, create_complete_organization (+3 more)

**Functions:**
- `generate_html_script_tag(json_ld) -> str` - Line 311

**Key Imports:** `datetime`, `integrity_studio_schema_types`, `json`, `pathlib`, `typing` (+1 more)

### `integrity_studio_schema_types.py` (python)

**Classes:**
- `ServiceType` (extends: str, Enum) - Line 27
  - Types of AI services offered
- `ActivityType` (extends: str, Enum) - Line 37
  - User activity types
- `RoleType` (extends: str, Enum) - Line 47
  - User role types
- `Thing` (extends: BaseModel) - Line 59
  - Base Schema.org Thing type
- `PostalAddress` (extends: BaseModel) - Line 79
  - Schema.org PostalAddress
- `Country` (extends: BaseModel) - Line 94
  - Schema.org Country
- `Person` (extends: Thing) - Line 109
  - Schema.org Person
- `ContactPoint` (extends: BaseModel) - Line 124
  - Schema.org ContactPoint
- `ImageObject` (extends: BaseModel) - Line 143
  - Schema.org ImageObject
- `PriceSpecification` (extends: BaseModel) - Line 160
  - Schema.org PriceSpecification
- `Offer` (extends: BaseModel) - Line 174
  - Schema.org Offer
- `Audience` (extends: BaseModel) - Line 191
  - Schema.org Audience
- `Service` (extends: Thing) - Line 203
  - Schema.org Service
- `OfferCatalog` (extends: BaseModel) - Line 217
  - Schema.org OfferCatalog
- `Organization` (extends: Thing) - Line 234
  - Schema.org Organization
- `ProfessionalService` (extends: Thing) - Line 257
  - Schema.org ProfessionalService
- `EntryPoint` (extends: BaseModel) - Line 277
  - Schema.org EntryPoint
- `SearchAction` (extends: BaseModel) - Line 288
  - Schema.org SearchAction
- `WebSite` (extends: Thing) - Line 300
  - Schema.org WebSite
- `WebPage` (extends: Thing) - Line 312
  - Schema.org WebPage
- `ListItem` (extends: BaseModel) - Line 325
  - Schema.org ListItem
- `BreadcrumbList` (extends: BaseModel) - Line 338
  - Schema.org BreadcrumbList
- `User` (extends: BaseModel) - Line 354
  - User model from Prisma schema
- `UserProfile` (extends: BaseModel) - Line 373
  - User profile model from Prisma schema
- `Role` (extends: BaseModel) - Line 392
  - Role model from Prisma schema
- `UserRole` (extends: BaseModel) - Line 404
  - User role assignment from Prisma schema
- `UserSession` (extends: BaseModel) - Line 415
  - User session model from Prisma schema
- `UserActivity` (extends: BaseModel) - Line 435
  - User activity tracking from Prisma schema
- `IntegrityStudioOrganization` (extends: Organization) - Line 453
  - Complete Integrity Studio organization model
- `IntegrityStudioService` (extends: Service) - Line 472
  - Enhanced service model with pricing

**Functions:**
- `create_integrity_studio_organization() -> IntegrityStudioOrganization` - Line 482
- `create_all_services() -> List[...]` - Line 574
- `export_to_json_ld(obj) -> dict` - Line 696

**Key Imports:** `datetime`, `decimal`, `enum`, `json`, `pydantic` (+2 more)

### `leora_data_loader.py` (python)

**Classes:**
- `LeoraDataLoader` - Line 24
  - Loads and parses Leora data from CSV files
  - Methods: __init__, _parse_price, _parse_datetime, load_products, load_categories (+1 more)

**Functions:**
- `generate_product_json_ld(product) -> dict` - Line 204
- `export_all_to_json_ld(org, output_file) -> dict` - Line 244

**Key Imports:** `csv`, `datetime`, `decimal`, `json`, `leora_schema_types` (+2 more)

### `leora_schema_types.py` (python)

**Classes:**
- `DayOfWeek` (extends: str, Enum) - Line 26
  - Schema.org DayOfWeek enumeration
- `ServiceType` (extends: str, Enum) - Line 37
  - Types of home health services offered
- `ProductTier` (extends: str, Enum) - Line 45
  - Product/Service tier levels
- `PricingDuration` (extends: str, Enum) - Line 52
  - Pricing duration options
- `TaxClass` (extends: str, Enum) - Line 58
  - Tax classification for products
- `Thing` (extends: BaseModel) - Line 67
  - Base Schema.org Thing type
- `PostalAddress` (extends: BaseModel) - Line 87
  - Schema.org PostalAddress
- `GeoCoordinates` (extends: BaseModel) - Line 102
  - Schema.org GeoCoordinates
- `Place` (extends: Thing) - Line 114
  - Schema.org Place
- `City` (extends: Place) - Line 124
  - Schema.org City
- `State` (extends: Place) - Line 135
  - Schema.org State
- `OpeningHoursSpecification` (extends: BaseModel) - Line 147
  - Schema.org OpeningHoursSpecification
  - Methods: validate_time_format
- `Service` (extends: Thing) - Line 177
  - Schema.org Service
- `MonetaryAmount` (extends: BaseModel) - Line 197
  - Schema.org MonetaryAmount
- `Offer` (extends: BaseModel) - Line 209
  - Schema.org Offer
- `OfferCatalog` (extends: BaseModel) - Line 224
  - Schema.org OfferCatalog
- `Product` (extends: Thing) - Line 236
  - Schema.org Product
- `Organization` (extends: Thing) - Line 254
  - Schema.org Organization
- `LocalBusiness` (extends: Organization) - Line 269
  - Schema.org LocalBusiness
- `ProductVariant` (extends: BaseModel) - Line 291
  - Leora product variant with pricing options
- `ServiceCategory` (extends: BaseModel) - Line 315
  - Service category definition
- `ContactInformation` (extends: BaseModel) - Line 329
  - Contact information for the organization
  - Methods: validate_phone
- `LeoraHomeHealth` (extends: LocalBusiness) - Line 348
  - Complete schema.org representation of Leora Home Health organization

**Functions:**
- `create_leora_organization() -> LeoraHomeHealth` - Line 378
- `export_to_json_ld(obj) -> dict` - Line 491

**Key Imports:** `datetime`, `decimal`, `enum`, `json`, `pydantic` (+1 more)

### `luis_landscaping_data_loader.py` (python)

**Classes:**
- `LuisLandscapingDataLoader` - Line 23
  - Loads and manages Luis Landscaping data
  - Methods: __init__, load_business_config, _extract_value, _extract_services, create_sample_contact_forms (+4 more)

**Functions:**
- `generate_html_script_tag(json_ld) -> str` - Line 279

**Key Imports:** `datetime`, `json`, `luis_landscaping_schema_types`, `pathlib`, `re` (+1 more)

### `luis_landscaping_schema_types.py` (python)

**Classes:**
- `ServiceType` (extends: str, Enum) - Line 26
  - Types of services offered
- `DayOfWeek` (extends: str, Enum) - Line 35
  - Schema.org DayOfWeek enumeration
- `ContactType` (extends: str, Enum) - Line 46
  - Contact form message types
- `Thing` (extends: BaseModel) - Line 58
  - Base Schema.org Thing type
- `PostalAddress` (extends: BaseModel) - Line 78
  - Schema.org PostalAddress
- `GeoCoordinates` (extends: BaseModel) - Line 93
  - Schema.org GeoCoordinates
- `Place` (extends: Thing) - Line 105
  - Schema.org Place
- `OpeningHoursSpecification` (extends: BaseModel) - Line 120
  - Schema.org OpeningHoursSpecification
  - Methods: validate_time_format
- `Service` (extends: Thing) - Line 150
  - Schema.org Service
- `Offer` (extends: BaseModel) - Line 163
  - Schema.org Offer
- `OfferCatalog` (extends: BaseModel) - Line 176
  - Schema.org OfferCatalog
- `ContactPoint` (extends: BaseModel) - Line 192
  - Schema.org ContactPoint
- `Organization` (extends: Thing) - Line 205
  - Schema.org Organization
- `LocalBusiness` (extends: Organization) - Line 216
  - Schema.org LocalBusiness
- `ContactFormData` (extends: BaseModel) - Line 239
  - Contact form submission data
  - Methods: validate_phone
- `ValidationError` (extends: BaseModel) - Line 261
  - Form validation error
- `LuisLandscapingBusiness` (extends: LocalBusiness) - Line 271
  - Complete Luis Landscaping & Handyman Services business model
- `LuisLandscapingService` (extends: Service) - Line 285
  - Enhanced service model for Luis Landscaping
- `EntryPoint` (extends: BaseModel) - Line 441
  - Schema.org EntryPoint
- `SearchAction` (extends: BaseModel) - Line 452
  - Schema.org SearchAction
- `WebSite` (extends: Thing) - Line 464
  - Schema.org WebSite

**Functions:**
- `create_luis_landscaping_business() -> LuisLandscapingBusiness` - Line 295
- `create_all_services() -> List[...]` - Line 377
- `export_to_json_ld(obj) -> dict` - Line 476

**Key Imports:** `datetime`, `decimal`, `enum`, `json`, `pydantic` (+1 more)

### `schema_org.py` (python)

**Functions:**
- `get_software_application_schema(repository_name, version, author_name, author_email) -> Dict[...]` - Line 14
- `get_dataset_schema(data_type, repository_name, file_path, record_count) -> Dict[...]` - Line 95
- `get_creative_work_schema(chart_type, repository_name, file_path) -> Dict[...]` - Line 186
- `get_mcp_server_schema() -> Dict[...]` - Line 249
- `save_structured_data(schema_data, output_path) -> <ast.Constant object at 0x103fa9450>` - Line 289
- `generate_all_schemas(repository_name, output_dir) -> Dict[...]` - Line 298
- `get_jsonld_script_tag(schema_data) -> str` - Line 330
- `get_meta_tags(schema_data) -> List[...]` - Line 337

**Key Imports:** `datetime`, `json`, `os`, `typing`

### `schemas.py` (python)

**Classes:**
- `ChartType` (extends: str, Enum) - Line 14
  - Supported chart types.
- `PeriodType` (extends: str, Enum) - Line 22
  - Time period types for commit analysis.
- `CommitData` (extends: BaseModel) - Line 29
  - Individual commit data model.
- `CommitCount` (extends: BaseModel) - Line 45
  - Aggregated commit count for a specific time period.
  - Methods: validate_period_range
- `PlotConfig` (extends: BaseModel) - Line 64
  - Configuration for plot generation.
  - Methods: validate_hex_color
- `ChartConfig` (extends: BaseModel) - Line 86
  - Configuration for individual chart generation.
  - Methods: validate_filename
- `ChartRequest` (extends: BaseModel) - Line 103
  - MCP server chart generation request.
- `VisualizationConfig` (extends: BaseModel) - Line 112
  - Overall configuration for the visualization toolkit.
- `RepositoryInfo` (extends: BaseModel) - Line 121
  - Repository information for chart generation.
- `DataFile` (extends: BaseModel) - Line 130
  - Data file information.
- `MCPToolResponse` (extends: BaseModel) - Line 139
  - Response from MCP tool execution.
- `Config` - Line 39

**Functions:**
- `validate_commit_data_file(file_path) -> List[...]` - Line 149
- `create_default_chart_config(chart_type, repo_name) -> ChartConfig` - Line 193

**Key Imports:** `datetime`, `enum`, `os`, `pydantic`, `typing`

### `setup_enhanced.py` (python)

**Functions:**
- `check_python_version()` - Line 17
- `check_git_repository()` - Line 28
- `create_virtual_environment()` - Line 44
- `get_pip_command()` - Line 62
- `install_dependencies()` - Line 70
- `create_directory_structure()` - Line 113
- `make_scripts_executable()` - Line 128
- `test_imports()` - Line 151
- `initialize_database()` - Line 180
- `generate_example_configs()` - Line 204
- ... and 4 more functions

**Key Imports:** `json`, `os`, `pathlib`, `subprocess`, `sys` (+1 more)

---
*Generated by Schema Generator*