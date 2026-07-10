-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "kollektivvertrag",
    "soziale_stellung",
    "zeitreihe",
    "indexwerte_basis_2016"
FROM "statistics-austria-ogd-tli16kv-tli-108"
