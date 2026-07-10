-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("reporting_year" AS BIGINT) AS reporting_year,
    "divorce_dissolution_of_registered_partnership",
    "type_of_decision",
    "sex_of_partners",
    "number_of_divorces_dissolutions_of_registered_partnerships"
FROM "statistics-austria-ogd-schapaext-sch-apa-1"
