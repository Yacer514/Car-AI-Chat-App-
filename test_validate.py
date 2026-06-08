#!/usr/bin/env python3
"""
Test sector validation
"""

from validators import validate_sector
from fare_database import get_available_sectors

available_sectors = get_available_sectors()
print(f"Available sectors: {available_sectors}")
print()

test_sectors = ['margalla', 'aabpara', 'f-6', 'g-8']

for sector in test_sectors:
    result = validate_sector(sector)
    print(f"validate_sector('{sector}') = {result}")
