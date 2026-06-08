#!/usr/bin/env python3
"""
Test fare estimation (Updated)
"""

from fare_database import get_fare_estimate

# Test Islamabad to Islamabad
result1 = get_fare_estimate("bike", "F-6", "Centaurus Mall")
print(f"F-6 to Centaurus (Bike): {result1}")

# Test Rawalpindi to Islamabad
result2 = get_fare_estimate("car", "Saddar", "F-7")
print(f"Saddar to F-7 (Car): {result2}")

# Test Luxury
result3 = get_fare_estimate("luxury", "Bahria", "Airport")
print(f"Bahria to Airport (Luxury): {result3}")
