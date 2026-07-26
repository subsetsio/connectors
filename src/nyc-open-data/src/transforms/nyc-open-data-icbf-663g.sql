-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sample_id",
    "site",
    strptime("sample_start_date", '%m/%d/%Y')::DATE AS sample_start_date,
    strptime("date", '%m/%d/%Y')::DATE AS date,
    "start_time",
    "time",
    "analyte",
    "status",
    "final_result",
    "units",
    "water_treatment_plant",
    "wtp_group",
    "spdes_number"
FROM "nyc-open-data-icbf-663g"
