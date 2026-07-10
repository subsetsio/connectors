-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("reporting_year" AS BIGINT) AS reporting_year,
    "geburtsland_teilw_abo_ebene_3",
    "age_in_year_groups",
    "sex",
    "number_of_naturalisations"
FROM "statistics-austria-ogd-einbuergerungen-einbj-1"
