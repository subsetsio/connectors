-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each dimension is an independent group-by of works, so counts across different dimension values or dimension families are not additive.
-- caution: Several dimension families are limited by the OpenAlex group_by top-200 result cap for each year; absence from a year does not mean zero works.
SELECT
    "dimension",
    "dimension_key",
    "dimension_label",
    "publication_year",
    "works_count"
FROM "openalex-works-by-dimension-year"
