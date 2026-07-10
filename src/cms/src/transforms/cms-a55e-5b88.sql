-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "Measure Code" AS measure_code,
    "Measure Name" AS measure_name,
    "Score" AS score,
    "Footnote" AS footnote,
    "Date" AS date
FROM "cms-a55e-5b88"
