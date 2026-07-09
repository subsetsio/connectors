-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The FATS addendum encodes flow as M and X, unlike the parent TISMOS table which spells out imports and exports.
-- caution: The table is a fixed historical mode-3 commercial-presence addendum, not a continuing annual series.
SELECT
    "FLOW" AS flow,
    "REPORTER" AS reporter,
    "PARTNER" AS partner,
    "INDICATOR" AS indicator,
    CAST("YEAR" AS BIGINT) AS year,
    TRY_CAST("VALUE" AS DOUBLE) AS value,
    "METH" AS meth
FROM "wto-tismos-fats"
