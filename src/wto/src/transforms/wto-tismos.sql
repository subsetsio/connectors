-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Imports and exports are combined in one table; filter the flow column before directional analysis.
-- caution: The mode-of-supply dimension carries distinct measures for the same reporter, partner, indicator, and year.
SELECT
    "FLOW" AS flow,
    "REPORTER" AS reporter,
    "PARTNER" AS partner,
    "INDICATOR" AS indicator,
    CAST("YEAR" AS BIGINT) AS year,
    "MODE" AS mode,
    TRY_CAST("VALUE" AS DOUBLE) AS value,
    "METH" AS meth
FROM "wto-tismos"
