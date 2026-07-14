-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Values are reconciled trade flows by exporter, importer, HS product, and year; product nomenclature is fixed to the downloaded BACI edition. This very large table is published keyless because full key verification exceeds the harness memory limit.
SELECT
    "t",
    "i",
    "j",
    "k",
    "v",
    "q"
FROM "cepii-baci"
