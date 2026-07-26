-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST(raw."Data values" AS DOUBLE) AS data_values,
    raw."Data description" AS data_description,
    raw."Population" AS population,
    raw."Local Authority" AS local_authority,
    strptime(raw."Year ending", '%d/%m/%Y')::DATE AS year,
    raw."Notes" AS notes
FROM "statswales-d11ca4b4-2cc5-4695-924b-54152498e316" AS raw
