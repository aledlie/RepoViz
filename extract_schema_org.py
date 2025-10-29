#!/usr/bin/env python3
"""
Extract and analyze Schema.org structured data from websites.
"""

import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Any
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def fetch_webpage(url: str) -> str:
    """Fetch webpage content."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except (URLError, HTTPError) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return ""


def extract_jsonld_scripts(html: str) -> List[Dict[str, Any]]:
    """Extract all JSON-LD scripts from HTML."""
    jsonld_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    scripts = re.findall(jsonld_pattern, html, re.DOTALL | re.IGNORECASE)

    structured_data = []
    for script in scripts:
        try:
            data = json.loads(script.strip())
            structured_data.append(data)
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse JSON-LD: {e}", file=sys.stderr)
            continue

    return structured_data


def extract_meta_tags(html: str) -> Dict[str, str]:
    """Extract relevant meta tags from HTML."""
    meta_tags = {}

    patterns = {
        'title': r'<title[^>]*>(.*?)</title>',
        'description': r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        'og:title': r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\'](.*?)["\']',
        'og:description': r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\'](.*?)["\']',
        'og:type': r'<meta[^>]*property=["\']og:type["\'][^>]*content=["\'](.*?)["\']',
        'og:url': r'<meta[^>]*property=["\']og:url["\'][^>]*content=["\'](.*?)["\']',
        'og:image': r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\'](.*?)["\']',
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            meta_tags[key] = match.group(1).strip()

    return meta_tags


def analyze_schema_org_data(url: str) -> Dict[str, Any]:
    """Analyze Schema.org structured data from a website."""
    print(f"Fetching {url}...", file=sys.stderr)
    html = fetch_webpage(url)

    if not html:
        return {
            'url': url,
            'error': 'Failed to fetch webpage',
            'timestamp': datetime.now().isoformat()
        }

    jsonld_data = extract_jsonld_scripts(html)
    meta_tags = extract_meta_tags(html)

    analysis = {
        'url': url,
        'timestamp': datetime.now().isoformat(),
        'jsonld_count': len(jsonld_data),
        'jsonld_scripts': jsonld_data,
        'meta_tags': meta_tags,
        'schema_types': []
    }

    # Extract schema types
    for data in jsonld_data:
        if isinstance(data, dict):
            if '@type' in data:
                analysis['schema_types'].append(data['@type'])
            elif '@graph' in data and isinstance(data['@graph'], list):
                for item in data['@graph']:
                    if isinstance(item, dict) and '@type' in item:
                        analysis['schema_types'].append(item['@type'])

    return analysis


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_schema_org.py <URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    analysis = analyze_schema_org_data(url)

    # Output as JSON
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
