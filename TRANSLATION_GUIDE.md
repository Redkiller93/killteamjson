# Translation Guide for Kill Team JSON

This guide explains how to translate the Kill Team JSON dataset into other languages using the folder-based structure.

## Project Structure

The repository uses a folder-based structure where each language has its own directory:

```
killteamjson/
├── en/                          # English (base language)
│   ├── teams.json
│   ├── weapon_rules.json
│   ├── universal_equipment.json
│   ├── universal_actions.json
│   ├── mission_actions.json
│   └── ops_2025.json
├── es/                          # Spanish
│   ├── teams.json
│   ├── weapon_rules.json
│   └── ...
├── fr/                          # French
│   ├── teams.json
│   ├── weapon_rules.json
│   └── ...
├── tools/                       # Translation tooling
│   ├── validate_translation.py
│   ├── extract_translatables.py
│   ├── check_translation_completeness.py
│   ├── translate_to_spanish.py
│   └── translate_to_french.py
├── README.md
└── TRANSLATION_GUIDE.md
```

**Benefits of this structure:**
- ✅ Clear organization by language
- ✅ Easy to add new languages (just create a new folder)
- ✅ Maintains identical structure per language
- ✅ Consumers can load entire language folder
- ✅ Language-specific documentation possible
- ✅ No file naming conflicts

## Translation Principles

### What to Translate

**Fields that SHOULD be translated:**
- `killteamName` - Kill team display names
- `description` - All description fields (teams, abilities, ploys, equipment, etc.)
- `composition` - Kill team composition rules
- `opTypeName` - Operative type names
- `wepName` - Weapon names
- `profileName` - Weapon profile names
- `abilityName` - Ability names
- `ployName` - Ploy names
- `eqName` - Equipment names
- `optionName` - Option names
- `title` - Operation titles (in ops files)
- `name` - Action and weapon rule names
- `archetypes` - Archetype array values (e.g., "Security", "Seek & Destroy")
- `reveal` - Operation reveal conditions (in ops files)
- `additionalRules` - Additional rules text (in ops files)
- `victoryPoints` - Victory point conditions (in ops files)

**Fields that SHOULD NOT be translated:**
- All `*Id` fields (`killteamId`, `factionId`, `opTypeId`, `wepId`, etc.)
- `version` - Version identifier (keep format like "October '25")
- `file` - PDF URLs (may point to language-specific PDFs)
- `wepType` - Weapon type codes (`R`, `M`, `P`, `E`)
- `MOVE`, `APL`, `SAVE`, `WOUNDS` - Core stats
- `ATK`, `HIT`, `DMG` - Weapon stats
- `seq` - Ordering numbers
- `isDefault`, `isPublished`, `isHomebrew` - Boolean flags
- `keywords` - Game keywords (keep in English - see below)
- `WR` array structure - Weapon rule IDs reference `weapon_rules.json`
- `actions` arrays - Action IDs reference action files
- `team` - Kill team identifiers (in weapon_rules.json)
- `type` - Type identifiers (e.g., "universal", "mission", "tac-op")
- `AP` - Action Point costs (numbers)
- `basesize`, `amount` - Numeric values
- `effects` - Encoded effect strings

### Keywords Handling

The `keywords` field contains game terms that should remain in English for consistency with official Games Workshop terminology. These are used for matching and game logic.

**Recommendation:** Keep keywords in English (e.g., "ANGEL OF DEATH", "LEADER", "PSYKER")

If localization is needed for display purposes, consider:
1. Keeping the English keyword for game logic
2. Translating the display name separately (e.g., `opTypeName`)
3. Using a glossary for keyword translations in UI layers

## Official Games Workshop Terminology

When translating, **always prioritize official Games Workshop terminology** over direct translations. Official terminology ensures consistency with rulebooks, official PDFs, and community understanding.

### Examples of Official Terminology

**Spanish (es):**
- "Shoot" → "Disparar"
- "Fight" → "Combatir"
- "Operative" → "Operativo"
- "Space Marine" → "Marine Espacial"
- "Angels Of Death" → "Ángeles de la Muerte"
- "Critical success" → "Éxito crítico"
- "Kill Team" → "Kill Team" (often kept in English)

**French (fr):**
- "Shoot" → "Tirer"
- "Fight" → "Combattre"
- "Operative" → "Opératif"
- "Space Marine" → "Marine Spatial"
- "Angels Of Death" → "Anges de la Mort"
- "Critical success" → "Succès critique"
- "Kill Team" → "Kill Team" (often kept in English)

**Archetypes:**
- English: "Security", "Seek & Destroy", "Recon", "Infiltration"
- Spanish: "Seguridad", "Buscar y Destruir", "Reconocimiento", "Infiltración"
- French: "Sécurité", "Rechercher et Détruire", "Reconnaissance", "Infiltration"

### Finding Official Terminology

1. **Official PDFs**: Check Games Workshop's official Spanish/French PDFs on warhammer-community.com
2. **Rulebooks**: Reference official translated rulebooks
3. **Community**: Check established translations in the Kill Team community
4. **Glossary**: Maintain a glossary of standard translations for consistency

## Translation Workflow

### Step 1: Create Language Folder Structure

If creating a new language translation:

```bash
# Create new language folder (e.g., for German)
mkdir de

# Copy structure from English
cp en/*.json de/
```

The translation tools can also create this structure:
```bash
python tools/translate_to_spanish.py   # Creates es/ folder
python tools/translate_to_french.py    # Creates fr/ folder
```

### Step 2: Translate User-Facing Strings

For each JSON file in your language folder:

1. **Open the file** in your language folder (e.g., `es/teams.json`)
2. **Translate translatable fields** using official GW terminology
3. **Keep all IDs and structure identical** to the English version
4. **Preserve JSON structure** - same keys, same nesting, same order
5. **Maintain formatting** - preserve markdown syntax, line breaks, etc.

### Step 3: Validate Structure

After translating, validate that your translation matches the English structure:

```bash
# Validate a specific file
python tools/validate_translation.py en/teams.json es/teams.json

# Should output: "[OK] es/teams.json structure matches en/teams.json"
```

### Step 4: Check Translation Completeness

Check what percentage of the translation is complete:

```bash
# Check translation completeness
python tools/check_translation_completeness.py en/teams.json es/teams.json
```

This will report:
- Total translatable strings
- Number translated
- Missing translations
- Untranslated strings (same as English)

### Step 5: Extract Translatables (Optional)

To extract all translatable strings for translation services:

```bash
# Extract translatable strings
python tools/extract_translatables.py en/teams.json translatables.json

# This creates a JSON file with all translatable strings and their paths
```

This is useful for:
- Translation services (Google Translate API, DeepL, etc.)
- Professional translation workflows
- Translation memory tools

## Translation Tools

All tools are located in the `tools/` folder:

### `validate_translation.py`

Validates that a translated JSON file has identical structure to the English base.

**Usage:**
```bash
python tools/validate_translation.py <english_file> <translation_file>
```

**Example:**
```bash
python tools/validate_translation.py en/teams.json es/teams.json
```

**What it checks:**
- All keys from English exist in translation
- No extra keys in translation
- Array lengths match
- Types match (string vs array vs object)
- Structure hierarchy matches

### `check_translation_completeness.py`

Reports translation progress and identifies missing translations.

**Usage:**
```bash
python tools/check_translation_completeness.py <english_file> <translation_file>
```

**Example:**
```bash
python tools/check_translation_completeness.py en/weapon_rules.json es/weapon_rules.json
```

**Output:**
- Total translatable strings
- Number translated (percentage)
- List of missing translations
- List of potentially untranslated strings (same as English)

### `extract_translatables.py`

Extracts all translatable strings from a JSON file into a structured format.

**Usage:**
```bash
python tools/extract_translatables.py <json_file> [output_file]
```

**Example:**
```bash
python tools/extract_translatables.py en/teams.json teams_translatables.json
```

**Output:**
JSON file with all translatable strings and their paths, useful for translation services.

## Translation Quality Guidelines

### Official Terminology

- **Always use official Games Workshop terminology** when available
- Maintain consistency across all files
- Create and maintain a glossary of standard translations
- When in doubt, check official PDFs or rulebooks

### Markdown Formatting

- Preserve markdown syntax (`**bold**`, `*italic*`, etc.)
- Keep code blocks and formatting intact
- Translate content, not structure
- Maintain list formatting and hierarchy

### Special Characters

- Preserve measurement units (`"` for inches, `'` for feet)
- Preserve line breaks (`\n`, `\r`)
- Handle special punctuation appropriately for the language
- Use proper quotation marks for the language

### Numbers and Stats

- Keep all numeric values unchanged
- Preserve stat formats (e.g., `"3+"`, `"6\""`)
- Keep damage formats (e.g., `"3/5"` means 3 normal, 5 critical)

### IDs and References

- **Never translate IDs** - they're used for matching and references
- Keep all ID structures identical across languages
- Ensure action IDs, weapon rule IDs, etc. match exactly

## Example Translation

### English (`en/teams.json`):

```json
{
  "factionId": "IMP",
  "killteamId": "IMP-AOD",
  "version": "October '25",
  "killteamName": "Angels Of Death",
  "description": "Genetically modified transhuman warriors, Space Marines are amongst Humanity's most elite fighting forces.",
  "archetypes": ["Security", "Seek & Destroy"]
}
```

### Spanish (`es/teams.json`):

```json
{
  "factionId": "IMP",
  "killteamId": "IMP-AOD",
  "version": "October '25",
  "killteamName": "Ángeles de la Muerte",
  "description": "Guerriers transhumains génétiquement modifiés, les Space Marines font partie des forces de combat les plus élites de l'Humanité.",
  "archetypes": ["Seguridad", "Buscar y Destruir"]
}
```

**Note:**
- ✅ IDs remain unchanged (`factionId`, `killteamId`)
- ✅ Structure identical (same keys, same nesting)
- ✅ User-facing strings translated
- ✅ Archetypes translated
- ✅ Official GW terminology used

## Maintaining Translations

### When English Files Are Updated

When the English base files are updated:

1. **Identify changes**: Use diff tools or version control to see what changed
2. **Update structure**: Ensure translation files have the same structure updates
3. **Translate new content**: Translate any new user-facing strings
4. **Update existing translations**: Review and update if English text changed
5. **Validate**: Run validation tools to ensure structure still matches

### Version Tracking

- Translation files should track the same version as English files
- Indicate translation completeness (e.g., 95% translated)
- Document any missing translations clearly

### Contributing Translations

When contributing translations:

1. **Fork the repository**
2. **Create/update translations** in the appropriate language folder
3. **Validate structure** using the provided tools
4. **Check completeness** before submitting
5. **Create a pull request** with:
   - Description of what was translated
   - Completeness percentage
   - Notes on any terminology decisions


## Best Practices

1. **Start small**: Begin with smaller files (weapon_rules.json, universal_actions.json) before tackling teams.json
2. **Use official terminology**: Always prioritize Games Workshop's official translations
3. **Maintain consistency**: Use the same translation for the same term across all files
4. **Validate often**: Run validation tools frequently during translation
5. **Check completeness**: Use completeness checker to track progress
6. **Preserve structure**: Never change IDs, structure, or non-translatable fields
7. **Test loading**: Ensure consumers can load and use translated files correctly

## Getting Help

If you need help with translations:

1. Check official Games Workshop PDFs for terminology
2. Review the existing English files for structure reference
3. Use the translation tools to validate and check progress
4. Consult the Kill Team community for established translations
5. Open an issue for terminology questions or translation guidance

