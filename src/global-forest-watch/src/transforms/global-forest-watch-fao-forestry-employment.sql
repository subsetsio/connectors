-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "iso",
    "country",
    "desk_study",
    "year",
    "silviculture_and_other_fte",
    "logging_fte",
    "gathering_fte",
    "support_fte",
    "all_fte",
    "female_fte"
FROM "global-forest-watch-fao-forestry-employment"
