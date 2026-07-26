-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "coordinates",
    "intro_number",
    "enactment_date",
    "enactment_year",
    "enactment_number",
    "category",
    "borough",
    "new_name",
    "present_name",
    "limits",
    "zip_code",
    "introduced_by_council_members",
    "biographical_information",
    "notes"
FROM "nyc-open-data-ig76-wwag"
