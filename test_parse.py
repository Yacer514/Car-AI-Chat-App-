#!/usr/bin/env python3
"""
Test script to debug query parsing (Updated)
"""

from validators import parse_query
from fare_database import get_all_locations

# Test queries
test_queries = [
    "Savour Saddar se Centaurus kitna hoga?",
    "Pindi station to Blue Area bike fare",
    "F-6 to G-11 AC car price",
    "10km luxury ride cost"
]

print("Available locations sample:", get_all_locations()[:10])
print()

for query in test_queries:
    print(f"Testing: {query}")
    parsed = parse_query(query)
    print(f"Parsed: {parsed}")
    print(f"Vehicle: {parsed['vehicle_type']}, Loc1: {parsed['loc1']}, Loc2: {parsed['loc2']}, Dist: {parsed['distance']}")
    print()
