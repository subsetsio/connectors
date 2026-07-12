-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("mt_code_ur" AS BIGINT) AS mt_code_ur,
    "mt_lib_court",
    "mt_lib",
    "mt_adr_part_1",
    "mt_adr_part_2",
    "mt_code_post",
    "mt_bur_dist"
FROM "urssaf-sst-dpae"
