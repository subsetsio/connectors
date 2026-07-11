-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "INDICATOR" AS indicator,
    CAST("DECIMALS" AS BIGINT) AS decimals,
    "CONTEXTDATE" AS contextdate,
    "OBSERVEDDATEFROM" AS observeddatefrom,
    "OBSERVEDDATETO" AS observeddateto,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value
FROM "norges-bank-financial-indicators"
