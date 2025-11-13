#!/usr/bin/env python3
"""
Translate JSON files to Spanish using official Games Workshop terminology.
"""

import json
import sys
from pathlib import Path

# Official GW Spanish terminology dictionary
GW_TERMS = {
    # Actions
    "Shoot": "Disparar",
    "Fight": "Combatir",
    "Reposition": "Reposicionar",
    "Dash": "Carrera",
    "Fall Back": "Retirada",
    "Charge": "Carga",
    "Guard": "Vigilancia",
    
    # Game terms
    "operative": "operativo",
    "operatives": "operativos",
    "Kill Team": "Kill Team",  # Often kept in English
    "Space Marine": "Marine Espacial",
    "Angels Of Death": "Ángeles de la Muerte",
    
    # Keywords
    "LEADER": "LÍDER",
    
    # Weapon rules (commonly used terms)
    "Critical success": "Éxito crítico",
    "critical success": "éxito crítico",
    "critical successes": "éxitos críticos",
    "normal success": "éxito normal",
    "normal successes": "éxitos normales",
    "attack dice": "dados de ataque",
    "defence dice": "dados de defensa",
    "cover saves": "salvaciones de cobertura",
    
    # Status
    "incapacitated": "incapacitado",
    "activation": "activación",
    "counteraction": "contrataque",
    "turning point": "punto de inflexión",
}

def translate_text(text):
    """Translate text using GW terminology and proper Spanish translation."""
    if not isinstance(text, str):
        return text
    
    # Apply GW terminology replacements
    translated = text
    for en_term, es_term in GW_TERMS.items():
        # Case-insensitive replacement while preserving original case
        import re
        pattern = re.compile(re.escape(en_term), re.IGNORECASE)
        translated = pattern.sub(es_term, translated)
    
    # General translation patterns for common game terms
    # These would typically be done with a proper translation API,
    # but for now we'll handle key terminology
    
    return translated

def translate_value(value, field_name=""):
    """Recursively translate JSON values."""
    if isinstance(value, str):
        # Only translate certain fields
        if field_name in ['name', 'description', 'killteamName', 'opTypeName', 
                         'wepName', 'abilityName', 'ployName', 'eqName', 
                         'optionName', 'title', 'profileName', 'composition',
                         'reveal', 'additionalRules', 'victoryPoints']:
            # This is a placeholder - in production, you'd use a translation service
            # or manual translation with GW terminology
            return value  # For now, return as-is - will be translated manually
        return value
    elif isinstance(value, dict):
        return {k: translate_value(v, k) for k, v in value.items()}
    elif isinstance(value, list):
        # Check if list contains translatable strings (like archetypes)
        if field_name == 'archetypes' and value and isinstance(value[0], str):
            # Translate archetype names
            archetype_translations = {
                "Security": "Seguridad",
                "Seek & Destroy": "Buscar y Destruir",
                "Recon": "Reconocimiento",
                "Infiltration": "Infiltración"
            }
            return [archetype_translations.get(v, v) for v in value]
        return [translate_value(item, field_name) for item in value]
    else:
        return value

def translate_file(en_file, es_file):
    """Translate a JSON file from English to Spanish."""
    print(f"Translating {en_file}...")
    
    with open(en_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Translate the data
    translated = translate_value(data)
    
    # Write translated file
    with open(es_file, 'w', encoding='utf-8') as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)
    
    print(f"Created {es_file} (structure copied, ready for manual translation)")
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
    es_dir = Path('es')
    es_dir.mkdir(exist_ok=True)
    
    for filename in files:
        en_file = en_dir / filename
        es_file = es_dir / filename
        
        if en_file.exists():
            translate_file(en_file, es_file)
        else:
            print(f"Warning: {en_file} not found")

