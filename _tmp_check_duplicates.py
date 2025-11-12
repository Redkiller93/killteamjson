import json
from pathlib import Path
from collections import Counter

# Load weapon rules
weapon_rules_path = Path('weapon_rules.json')
with open(weapon_rules_path, 'r', encoding='utf-8') as f:
    weapon_rules_data = json.load(f)

# Check for duplicate IDs
all_ids = [rule['id'] for rule in weapon_rules_data['weapon_rules']]
id_counts = Counter(all_ids)
duplicates = {id: count for id, count in id_counts.items() if count > 1}

if duplicates:
    print(f'Found {len(duplicates)} duplicate IDs:')
    for dup_id, count in sorted(duplicates.items()):
        print(f'  {dup_id}: appears {count} times')
    
    # Find and show the duplicate entries
    print('\\nDuplicate entries:')
    for dup_id in duplicates:
        print(f'\\n  ID: {dup_id}')
        for i, rule in enumerate(weapon_rules_data['weapon_rules']):
            if rule['id'] == dup_id:
                rule_name = rule.get('name')
                rule_team = rule.get('team')
                print(f'    Entry {i}: name={rule_name}, team={rule_team}')
    
    # Remove duplicates, keeping the first occurrence
    seen_ids = set()
    unique_rules = []
    removed_count = 0
    
    for rule in weapon_rules_data['weapon_rules']:
        rule_id = rule['id']
        if rule_id not in seen_ids:
            seen_ids.add(rule_id)
            unique_rules.append(rule)
        else:
            removed_count += 1
            rule_name = rule.get('name')
            print(f'Removing duplicate: {rule_id} (name: {rule_name})')
    
    weapon_rules_data['weapon_rules'] = unique_rules
    
    # Save updated weapon rules
    with open(weapon_rules_path, 'w', encoding='utf-8') as f:
        json.dump(weapon_rules_data, f, indent=2, ensure_ascii=False)
    
    print(f'\\nRemoved {removed_count} duplicate entries')
    print(f'Total weapon rules after cleanup: {len(unique_rules)}')
else:
    print('No duplicate IDs found. All weapon rule IDs are unique.')
    print(f'Total weapon rules: {len(all_ids)}')
