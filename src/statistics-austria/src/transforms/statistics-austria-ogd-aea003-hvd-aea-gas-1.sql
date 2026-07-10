-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "economic_branch",
    "hfc_in_tons_co2_equivalents",
    "pfc_in_tons_co2_equivalents",
    "sf6_and_nf3_in_tons_co2_equivalents"
FROM "statistics-austria-ogd-aea003-hvd-aea-gas-1"
