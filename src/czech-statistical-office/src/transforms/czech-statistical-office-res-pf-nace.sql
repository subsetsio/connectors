-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified for this upstream table; treat rows as source observations and avoid assuming uniqueness without applying source-specific dimensions.
SELECT
    "ICO" AS ico,
    CAST("ZDRUD" AS BIGINT) AS zdrud,
    CAST("KODCIS" AS BIGINT) AS kodcis,
    "HODN" AS hodn,
    strptime("DATPLAT", '%Y-%m-%d')::DATE AS datplat,
    strptime("DDATPAKT", '%Y-%m-%d')::DATE AS ddatpakt,
    "PRIZNAK" AS priznak
FROM "czech-statistical-office-res-pf-nace"
