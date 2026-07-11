-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "STEM status sex educational level employment sector and occupation" AS stem_status_sex_educational_level_employment_sector_and_occupation,
    "Total number" AS total_number,
    "Median dollars" AS median_dollars
FROM "ncses-nsf25323-tab009"
