import os
TESTS = "/Users/nathansnellaert/Documents/hardened/connectors/src/sea-around-us/tests"
os.makedirs(TESTS, exist_ok=True)

MEASURES = ("tonnage", "value")
DIMS = ["taxon","commercialgroup","functionalgroup","country","sector","catchtype","reporting-status"]

CATCH_TMPL = '''spec_id: {sid}
status: active
tests:
  - not_null: region_type
  - not_null: region_id
  - column_type: {{col: region_id, type: integer}}
  - not_null: category
    reason: every catch series carries a breakdown label (taxon/group/sector/etc)
  - not_null: year
  - column_type: {{col: year, type: integer}}
  - not_null: value
    reason: rows with a null amount are dropped during fetch
  - column_type: {{col: value, type: float}}
  - at_least: {{col: year, expr: 1950}}
    reason: the reconstruction starts in 1950
    certainty: 95
  - at_most: {{col: year, expr: current_year()}}
    reason: catch is historical; a future year means a parsing/units error or source projections
    certainty: 80
    points_outward: true
    severity: warn
  - at_least: {{col: value, expr: 0}}
    reason: catch weight and landed value are non-negative
    certainty: 85
    severity: warn
  - distinct_count: {{col: region_type, min: 1, max: 4}}
    reason: we enumerate eez, lme, rfmo and global only
    certainty: 85
  - enum: {{col: region_type, values: [eez, lme, rfmo, global]}}
    certainty: 90
'''

for m in MEASURES:
    for d in DIMS:
        sid = f"sea-around-us-catch-{m}-by-{d}"
        with open(f"{TESTS}/{sid}.yaml", "w") as f:
            f.write(CATCH_TMPL.format(sid=sid))

TAXA = '''spec_id: sea-around-us-taxa
status: active
tests:
  - not_null: taxon_key
  - column_type: {col: taxon_key, type: integer}
  - unique: taxon_key
    reason: taxon_key is the primary identifier; dupes mean the list was concatenated twice
    certainty: 95
  - not_null: scientific_name
    reason: every taxon record has a scientific name
    certainty: 90
  - row_count: {min: 2000}
    reason: the taxa list had ~3532 records when probed; <2000 means a truncated fetch
    certainty: 90
  - distinct_count: {col: taxon_key, min: 2000}
    certainty: 90
'''
with open(f"{TESTS}/sea-around-us-taxa.yaml", "w") as f:
    f.write(TAXA)

print("wrote", len(os.listdir(TESTS)), "yaml files")
