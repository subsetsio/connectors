-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code",
    "definition",
    "manhattan_96th_st_below",
    "all_other_areas"
FROM "nyc-open-data-ncbg-6agr"
