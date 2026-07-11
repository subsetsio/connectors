-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "All visual and performing arts fields" AS all_visual_and_performing_arts_fields,
    "Performing arts" AS performing_arts,
    "Visual arts media studies and design" AS visual_arts_media_studies_and_design
FROM "ncses-nsf25349-tab008-017"
