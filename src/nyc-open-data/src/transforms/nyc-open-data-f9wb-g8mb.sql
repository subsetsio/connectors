-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin",
    "system_id",
    "address",
    "borough",
    "zip_code",
    "status",
    "active_equip",
    "inspection_date",
    "violation_code",
    "law_section",
    "violation_text",
    "violation_type",
    "citation_text",
    "summons_number",
    "inspection_type",
    "bbl",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "nta_code"
FROM "nyc-open-data-f9wb-g8mb"
