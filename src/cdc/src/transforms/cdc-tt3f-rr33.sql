-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Jurisdiction" AS jurisdiction,
    "Sub-Jurisdiction" AS sub_jurisdiction,
    "Topical Area" AS topical_area,
    "Supplemental Act Name" AS supplemental_act_name,
    "Award Name" AS award_name,
    CAST("Amount" AS BIGINT) AS amount
FROM "cdc-tt3f-rr33"
