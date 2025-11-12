import json
from pathlib import Path
import re

# Load weapon rules
weapon_rules_path = Path('weapon_rules.json')
with open(weapon_rules_path, 'r', encoding='utf-8') as f:
    weapon_rules_data = json.load(f)

existing_ids = {rule['id'] for rule in weapon_rules_data['weapon_rules']}

# Load teams.json
teams_path = Path('teams.json')
with open(teams_path, 'r', encoding='utf-8') as f:
    teams = json.load(f)

# Collect all WR IDs and check if they have numbers (variable)
wr_info = {}  # id -> {has_number: bool, name: str or None}

def collect_wr_info(obj):
    if isinstance(obj, dict):
        if 'WR' in obj and isinstance(obj['WR'], list):
            for wri in obj['WR']:
                if isinstance(wri, dict) and 'id' in wri:
                    wr_id = wri['id']
                    if wr_id not in existing_ids:
                        if wr_id not in wr_info:
                            wr_info[wr_id] = {
                                'has_number': False,
                                'name': wri.get('name')
                            }
                        if wri.get('number') is not None:
                            wr_info[wr_id]['has_number'] = True
        for value in obj.values():
            collect_wr_info(value)
    elif isinstance(obj, list):
        for item in obj:
            collect_wr_info(item)

collect_wr_info(teams)

def id_to_name(wr_id):
    """Convert WR ID to a readable name"""
    # Remove WR- prefix
    name = wr_id.replace('WR-', '')
    # Remove asterisk prefix if present
    if name.startswith('*'):
        name = name[1:]
    # Replace hyphens with spaces
    name = name.replace('-', ' ')
    # Convert to title case
    name = name.title()
    return name

# Create new weapon rule entries
new_rules = []
for wr_id in sorted(wr_info.keys()):
    info = wr_info[wr_id]
    name = info['name'] if info['name'] else id_to_name(wr_id)
    
    new_rule = {
        'id': wr_id,
        'name': name,
        'variable': info['has_number'],
        'description': '',
        'universal': False
    }
    new_rules.append(new_rule)

# Add new rules to weapon_rules_data
weapon_rules_data['weapon_rules'].extend(new_rules)

# Save updated weapon rules
with open(weapon_rules_path, 'w', encoding='utf-8') as f:
    json.dump(weapon_rules_data, f, indent=2, ensure_ascii=False)

print(f'Added {len(new_rules)} new weapon rule entries')
print('New entries:')
for rule in new_rules:
    rule_id = rule['id']
    rule_name = rule['name']
    rule_var = rule['variable']
    print(f'  {rule_id} - {rule_name} (variable: {rule_var})')
