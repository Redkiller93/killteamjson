import json
from pathlib import Path
import re

# Load weapon rules
weapon_rules_path = Path('weapon_rules.json')
with open(weapon_rules_path, 'r', encoding='utf-8') as f:
    weapon_rules_data = json.load(f)

# Load teams.json
teams_path = Path('teams.json')
with open(teams_path, 'r', encoding='utf-8') as f:
    teams = json.load(f)

# Build mapping of weapon rule name to weapon rule object
# Extract rule name from ID (e.g., WR-NEC-HIER-MAGNIFY -> MAGNIFY)
weapon_rule_map = {}
for rule in weapon_rules_data['weapon_rules']:
    rule_id = rule['id']
    # Extract the rule name part (after team prefix)
    if rule_id.startswith('WR-UNIV-'):
        rule_name = rule_id.replace('WR-UNIV-', '')
    else:
        # Extract after team (e.g., WR-NEC-HIER-MAGNIFY -> MAGNIFY)
        parts = rule_id.split('-')
        if len(parts) >= 3:
            rule_name = '-'.join(parts[2:])  # Everything after WR-{TEAM}-
        else:
            rule_name = rule_id
    
    # Normalize for matching (uppercase, no special chars)
    normalized_name = rule_name.upper().replace('*', '')
    weapon_rule_map[normalized_name] = {
        'rule': rule,
        'original_name': rule_name,
        'team': rule.get('team')
    }

# Find abilities that match weapon rules
abilities_to_remove = []
descriptions_to_copy = {}

def find_matching_abilities(obj, current_killteam_id=None):
    if isinstance(obj, dict):
        # Track current killteamId
        if 'killteamId' in obj:
            current_killteam_id = obj['killteamId']
        
        # Check abilities array
        if 'abilities' in obj and isinstance(obj['abilities'], list):
            for ability in obj['abilities']:
                if not isinstance(ability, dict):
                    continue
                
                ability_id = ability.get('abilityId', '')
                ability_name = ability.get('abilityName', '')
                ability_desc = ability.get('description', '')
                
                if not ability_name or not ability_desc:
                    continue
                
                # Normalize ability name (remove asterisk, uppercase)
                normalized_ability_name = ability_name.replace('*', '').upper()
                
                # Try to match with weapon rules
                for norm_wr_name, wr_info in weapon_rule_map.items():
                    # Check if ability name contains weapon rule name
                    if norm_wr_name in normalized_ability_name or normalized_ability_name in norm_wr_name:
                        # Check if team matches
                        wr_team = wr_info['team']
                        if wr_team is None or wr_team == current_killteam_id:
                            # Found a match!
                            wr_rule = wr_info['rule']
                            wr_id = wr_rule['id']
                            
                            # Store description to copy
                            if wr_id not in descriptions_to_copy:
                                descriptions_to_copy[wr_id] = ability_desc
                            
                            # Mark ability for removal
                            abilities_to_remove.append({
                                'ability': ability,
                                'parent': obj,
                                'weapon_rule_id': wr_id,
                                'ability_name': ability_name
                            })
                            break
        
        # Recursively process all values
        for value in obj.values():
            find_matching_abilities(value, current_killteam_id)
    elif isinstance(obj, list):
        for item in obj:
            find_matching_abilities(item, current_killteam_id)

find_matching_abilities(teams)

print(f'Found {len(descriptions_to_copy)} weapon rules with matching abilities')
print(f'Found {len(abilities_to_remove)} abilities to remove')

# Copy descriptions to weapon rules
for wr_id, description in descriptions_to_copy.items():
    for rule in weapon_rules_data['weapon_rules']:
        if rule['id'] == wr_id:
            rule['description'] = description
            print(f'Updated description for {wr_id}')

# Remove abilities from teams.json
for item in abilities_to_remove:
    parent = item['parent']
    ability = item['ability']
    if 'abilities' in parent and isinstance(parent['abilities'], list):
        if ability in parent['abilities']:
            parent['abilities'].remove(ability)
            ab_name = item['ability_name']
            wr_id = item['weapon_rule_id']
            print(f'Removed ability {ab_name} (matching {wr_id})')

# Save updated files
with open(weapon_rules_path, 'w', encoding='utf-8') as f:
    json.dump(weapon_rules_data, f, indent=2, ensure_ascii=False)

with open(teams_path, 'w', encoding='utf-8') as f:
    json.dump(teams, f, indent=2, ensure_ascii=False)

print('\\nDone!')
