#!/usr/bin/env python3
"""
Debug utility: Compare TIFF tags between original and converted files.
Usage: python compare_tags.py <original.tif> <converted.tif>
"""

import sys
import tifffile


def compare_tiff_tags(orig_path, new_path):
    """Compare tags in two TIFF files."""
    print(f'Original file: {orig_path}')
    print('Original tags:')
    try:
        with tifffile.TiffFile(orig_path) as t:
            for tag in t.pages[0].tags.values():
                print(f"  {tag.code:3d} {tag.name:30s} {type(tag.value).__name__}")
    except Exception as e:
        print(f"  Error reading: {e}")
        return False
    
    print(f'\nNew file: {new_path}')
    print('New tags:')
    try:
        with tifffile.TiffFile(new_path) as t:
            for tag in t.pages[0].tags.values():
                print(f"  {tag.code:3d} {tag.name:30s} {type(tag.value).__name__}")
    except Exception as e:
        print(f"  Error reading: {e}")
        return False
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_tags.py <original.tif> <converted.tif>")
        print("\nThis utility compares TIFF metadata tags between original and converted files.")
        sys.exit(1)
    
    orig = sys.argv[1]
    new = sys.argv[2]
    
    success = compare_tiff_tags(orig, new)
    sys.exit(0 if success else 1)
