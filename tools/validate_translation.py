#!/usr/bin/env python3
"""
Validate that a translated JSON file has identical structure to the English base file.
"""

import json
import sys
from pathlib import Path

def compare_structures(en_data, trans_data, path="", errors=None):
    """Recursively compare two JSON structures."""
    if errors is None:
        errors = []
    
    # Check if both are the same type
    if type(en_data) != type(trans_data):
        errors.append(f"{path}: Type mismatch - English: {type(en_data).__name__}, Translation: {type(trans_data).__name__}")
        return errors
    
    if isinstance(en_data, dict):
        # Check all keys from English exist in translation
        for key in en_data:
            full_path = f"{path}.{key}" if path else key
            if key not in trans_data:
                errors.append(f"{full_path}: Missing in translation")
            else:
                compare_structures(en_data[key], trans_data[key], full_path, errors)
        
        # Check for extra keys in translation
        for key in trans_data:
            if key not in en_data:
                errors.append(f"{path}.{key}: Extra key in translation (not in English)")
    
    elif isinstance(en_data, list):
        if len(en_data) != len(trans_data):
            errors.append(f"{path}: Array length mismatch - English: {len(en_data)}, Translation: {len(trans_data)}")
        else:
            for i, (en_item, trans_item) in enumerate(zip(en_data, trans_data)):
                compare_structures(en_item, trans_item, f"{path}[{i}]", errors)
    
    # For primitives (string, int, bool, null), we don't compare values
    # Only structure matters
    
    return errors

def validate_translation(english_file, translation_file):
    """Validate a translation file against the English base."""
    try:
        with open(english_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
    except Exception as e:
        print(f"Error reading English file: {e}")
        return False
    
    try:
        with open(translation_file, 'r', encoding='utf-8') as f:
            trans_data = json.load(f)
    except Exception as e:
        print(f"Error reading translation file: {e}")
        return False
    
    # Compare structures
    errors = compare_structures(en_data, trans_data)
    
    if errors:
        print(f"\n[ERROR] Structure validation failed for {translation_file}")
        print(f"Found {len(errors)} structural differences:\n")
        for error in errors[:50]:  # Limit to first 50 errors
            print(f"  - {error}")
        if len(errors) > 50:
            print(f"\n  ... and {len(errors) - 50} more errors")
        return False
    else:
        print(f"[OK] {translation_file} structure matches {english_file}")
        return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_translation.py <english_file> <translation_file>")
        print("Example: python validate_translation.py teams.json teams.fr.json")
        sys.exit(1)
    
    english_file = sys.argv[1]
    translation_file = sys.argv[2]
    
    if not Path(english_file).exists():
        print(f"Error: English file not found: {english_file}")
        sys.exit(1)
    
    if not Path(translation_file).exists():
        print(f"Error: Translation file not found: {translation_file}")
        sys.exit(1)
    
    success = validate_translation(english_file, translation_file)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

