-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "asOfDate" AS asofdate,
    CAST("bills" AS BIGINT) AS bills,
    CAST("notesbonds" AS BIGINT) AS notesbonds,
    CAST("tips" AS BIGINT) AS tips,
    "frn",
    CAST("tipsInflationCompensation" AS DOUBLE) AS tipsinflationcompensation,
    CAST("mbs" AS DOUBLE) AS mbs,
    CAST("cmbs" AS DOUBLE) AS cmbs,
    "agencies",
    CAST("total" AS DOUBLE) AS total
FROM "ny-fed-soma-summary"
