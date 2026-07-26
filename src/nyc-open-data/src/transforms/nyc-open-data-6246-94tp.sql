-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inspection_stage_description",
    "school_code",
    "borough_name",
    "tco_obtained_date",
    "inspection_category",
    "observation_description",
    "inspection_date"
FROM "nyc-open-data-6246-94tp"
