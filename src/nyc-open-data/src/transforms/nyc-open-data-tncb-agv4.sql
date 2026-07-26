-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grade_band",
    "activity",
    "description",
    "target_population",
    "category"
FROM "nyc-open-data-tncb-agv4"
