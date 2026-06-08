#!/usr/bin/env python3
"""
Test sector info
"""

from fare_database import get_sector_info

info1 = get_sector_info("Margalla")
info2 = get_sector_info("Aabpara")

print(f"Sector info for Margalla: {info1}")
print(f"Sector info for Aabpara: {info2}")
