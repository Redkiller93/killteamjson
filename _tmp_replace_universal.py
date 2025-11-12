import json
from pathlib import Path
from collections import defaultdict

# Load weapon rules
weapon_rules_path = Path('weapon_rules.json')
with open(weapon_rules_path, 'r', encoding='utf-8') as f:
    weapon_rules_data = json.load(f)

# Identify universal rules (those with universal: true)
universal_rule_ids = {rule['id'] for rule in weapon_rules_data['weapon_rules'] if rule.get('universal') == True}

# Load teams.json to find which killteamId uses each non-universal rule
teams_path = Path('teams.json')
with open(teams_path, 'r', encoding='utf-8') as f:
    teams = json.load(f)

# Map non-universal rule IDs to killteamIds
rule_to_killteam = defaultdict(set)

def find_rule_killteams(obj, current_killteam_id=None):
    if isinstance(obj, dict):
        # Track current killteamId
        if 'killteamId' in obj:
            current_killteam_id = obj['killteamId']
        
        # Check WR arrays
        if 'WR' in obj and isinstance(obj['WR'], list):
            for wri in obj['WR']:
                if isinstance(wri, dict) and 'id' in wri:
                    wr_id = wri['id']
                    if wr_id not in universal_rule_ids and current_killteam_id:
                        rule_to_killteam[wr_id].add(current_killteam_id)
        
        # Recursively process all values
        for value in obj.values():
            find_rule_killteams(value, current_killteam_id)
    elif isinstance(obj, list):
        for item in obj:
            find_rule_killteams(item, current_killteam_id)

find_rule_killteams(teams)

# Update weapon rules
for rule in weapon_rules_data['weapon_rules']:
    # Remove universal key
    if 'universal' in rule:
        del rule['universal']
    
    # Add team key
    rule_id = rule['id']
    if rule_id in universal_rule_ids:
        rule['team'] = None
    else:
        # Get the killteamId(s) for this rule
        killteam_ids = rule_to_killteam.get(rule_id, set())
        if len(killteam_ids) == 1:
            rule['team'] = list(killteam_ids)[0]
        elif len(killteam_ids) > 1:
            # Multiple killteams use this rule - use the first one or None?
            # Let's use the first one alphabetically for consistency
            rule['team'] = sorted(killteam_ids)[0]
        else:
            # No killteam found - set to null
            rule['team'] = None

# Save updated weapon rules
with open(weapon_rules_path, 'w', encoding='utf-8') as f:
    json.dump(weapon_rules_data, f, indent=2, ensure_ascii=False)

total_rules = len(weapon_rules_data['weapon_rules'])
universal_count = sum(1 for r in weapon_rules_data['weapon_rules'] if r.get('team') is None)
team_specific_count = sum(1 for r in weapon_rules_data['weapon_rules'] if r.get('team') is not None)
print(f'Updated {total_rules} weapon rules')
print(f'Universal rules (team: null): {universal_count}')
print(f'Team-specific rules: {team_specific_count}')
