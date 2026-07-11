-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "paho_indicator_id",
    "indicator_name",
    "nombre_indicador"
FROM "paho-core-indicators"
