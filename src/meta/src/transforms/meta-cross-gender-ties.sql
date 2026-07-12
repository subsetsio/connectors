-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is a regional aggregate of cross-gender social ties, not an individual-level observation.
SELECT
    "region_id",
    "region_name",
    "country",
    "level",
    "cgfr_5",
    "cgfr_10",
    "cgfr_25",
    "cgfr_50",
    "cgfr_75",
    "cgfr_100",
    "cgfr_125",
    "cgfr_150",
    "cgfr_175",
    "cgfr_200",
    "_source_file" AS source_file
FROM "meta-cross-gender-ties"
