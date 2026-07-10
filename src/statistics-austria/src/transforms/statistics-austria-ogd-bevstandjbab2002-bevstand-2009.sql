-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "sex",
    "commune_aggregation_by_political_district",
    "age_in_single_years",
    "number"
FROM "statistics-austria-ogd-bevstandjbab2002-bevstand-2009"
