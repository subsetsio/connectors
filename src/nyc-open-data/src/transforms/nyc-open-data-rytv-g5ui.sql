-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin",
    "house",
    "street_name",
    "zip_code",
    "borough",
    "status",
    "number_of_dwt",
    "activity_type",
    "activity_year",
    "violation_code",
    "law_section",
    "violation_text",
    "compliance_year",
    "date_of_occurrence",
    "summons_number",
    "bbl",
    "longitude",
    "latitude",
    "community_board",
    "council_district",
    "census_tract",
    "nta_code"
FROM "nyc-open-data-rytv-g5ui"
