-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Collection Year (at 31 March)" AS collection_year_at_31_march,
    "Local Authority" AS local_authority,
    "Notes" AS notes
FROM "statswales-3014f5e6-f6fc-4725-98c5-ad9618f6166d"
