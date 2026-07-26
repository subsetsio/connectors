-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "adc_persons",
    "adcu_persons",
    "afdc_persons",
    "tanf_recipients",
    "hrpg_persons",
    "hr_exclud_pgadc_persons",
    "hr_persons",
    "afdc",
    "sn_recipients",
    "duplicated_count_ca_persons",
    "unduplicated_count_ca_persons"
FROM "nyc-open-data-thqd-deec"
