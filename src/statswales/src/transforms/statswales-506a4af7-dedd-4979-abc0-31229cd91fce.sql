-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Unitary Authority" AS unitary_authority,
    "Service" AS service,
    "Notes" AS notes
FROM "statswales-506a4af7-dedd-4979-abc0-31229cd91fce"
