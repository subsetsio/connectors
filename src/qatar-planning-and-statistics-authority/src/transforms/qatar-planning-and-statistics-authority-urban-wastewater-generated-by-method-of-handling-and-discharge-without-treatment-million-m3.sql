-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_name",
    "sm_lmw_shr",
    "value_million_cubic_metre"
FROM "qatar-planning-and-statistics-authority-urban-wastewater-generated-by-method-of-handling-and-discharge-without-treatment-million-m3"
