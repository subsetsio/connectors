-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly state emissions are departing-trajectory estimates and should not be treated as airport-level or arrival-emissions measures.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH" AS BIGINT) AS month,
    "STATE_NAME" AS state_name,
    "STATE_CODE" AS state_code,
    CAST("NOTE" AS BOOLEAN) AS note,
    CAST("CO2_QTY_TONNES" AS DOUBLE) AS co2_qty_tonnes,
    CAST("TF" AS BIGINT) AS tf,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-co2-emmissions-by-state"
