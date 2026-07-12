-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Iwi_affiliation_code" AS iwi_affiliation_code,
    "Iwi_affiliation_description" AS iwi_affiliation_description,
    "Estimated_count" AS estimated_count,
    "Iwi_grouping_code" AS iwi_grouping_code,
    "Iwi_grouping_description" AS iwi_grouping_description
FROM "statsnz-iwi-affiliation-estimated-counts-2018-csv"
