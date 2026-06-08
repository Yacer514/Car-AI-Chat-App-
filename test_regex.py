#!/usr/bin/env python3
"""
Test regex pattern
"""

import re

query_lower = "what's the fare for a bike from margalla to aabpara?"
sector_pattern = r'[a-z]-\d{1,2}|aabpara|margalla|shalimar|bahria|koral|chakri|rawal'
matches = re.findall(sector_pattern, query_lower)

print(f"Query: {query_lower}")
print(f"Pattern: {sector_pattern}")
print(f"Matches: {matches}")
