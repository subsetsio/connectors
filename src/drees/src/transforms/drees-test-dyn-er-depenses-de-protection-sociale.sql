-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pays",
    "depenses_en_2007",
    "depenses_en_2023"
FROM "drees-test-dyn-er-depenses-de-protection-sociale"
