#!/usr/bin/env python3
"""
Translate JSON files to French using official Games Workshop terminology.
Creates French versions with proper GW French terminology.
"""

import json
import sys
from pathlib import Path

# Official GW French terminology dictionary
GW_FR_TERMS = {
    # Actions
    "Shoot": "Tirer",
    "Fight": "Combattre",
    "Reposition": "Repositionner",
    "Dash": "Ruée",
    "Fall Back": "Repli",
    "Charge": "Charge",
    "Guard": "Vigilance",
    
    # Game terms
    "operative": "opératif",
    "operatives": "opératifs",
    "Kill Team": "Kill Team",  # Often kept in English
    "Space Marine": "Marine Spatial",
    "Angels Of Death": "Anges de la Mort",
    
    # Keywords
    "LEADER": "CHEF",
    
    # Weapon rules
    "Critical success": "Succès critique",
    "critical success": "succès critique",
    "critical successes": "succès critiques",
    "normal success": "succès normal",
    "normal successes": "succès normaux",
    "attack dice": "dés d'attaque",
    "defence dice": "dés de défense",
    "cover saves": "sauvegardes de couverture",
    
    # Status
    "incapacitated": "hors de combat",
    "activation": "activation",
    "counteraction": "contre-attaque",
    "turning point": "point tournant",
}

# Archetype translations
ARCHETYPE_TRANSLATIONS = {
    "Security": "Sécurité",
    "Seek & Destroy": "Rechercher et Détruire",
    "Recon": "Reconnaissance",
    "Infiltration": "Infiltration"
}

def translate_value(value, field_name=""):
    """Recursively translate JSON values using GW French terminology."""
    if isinstance(value, str):
        # Only translate certain fields
        if field_name in ['name', 'description', 'killteamName', 'opTypeName', 
                         'wepName', 'abilityName', 'ployName', 'eqName', 
                         'optionName', 'title', 'profileName', 'composition',
                         'reveal', 'additionalRules', 'victoryPoints', 'eqName']:
            # For now, return as-is - will need manual/proper translation
            # This is a placeholder structure
            return value  # Placeholder
        return value
    elif isinstance(value, dict):
        return {k: translate_value(v, k) for k, v in value.items()}
    elif isinstance(value, list):
        # Check if list contains translatable strings (like archetypes)
        if field_name == 'archetypes' and value and isinstance(value[0], str):
            return [ARCHETYPE_TRANSLATIONS.get(v, v) for v in value]
        return [translate_value(item, field_name) for item in value]
    else:
        return value

def translate_file(en_file, fr_file):
    """Copy structure from English to French (ready for translation)."""
    print(f"Creating French structure for {en_file.name}...")
    
    with open(en_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Translate structure (this is a placeholder - actual translation needed)
    translated = translate_value(data)
    
    # Write French file
    with open(fr_file, 'w', encoding='utf-8') as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)
    
    print(f"Created {fr_file} (structure copied, ready for French translation)")
    return translated

if __name__ == '__main__':
    # Files to translate
    files = [
        'weapon_rules.json',
        'universal_equipment.json',
        'universal_actions.json',
        'mission_actions.json',
        'ops_2025.json',
        'teams.json'
    ]
    
    en_dir = Path('en')
    fr_dir = Path('fr')
    fr_dir.mkdir(exist_ok=True)
    
    for filename in files:
        en_file = en_dir / filename
        fr_file = fr_dir / filename
        
        if en_file.exists():
            translate_file(en_file, fr_file)
        else:
            print(f"Warning: {en_file} not found")

