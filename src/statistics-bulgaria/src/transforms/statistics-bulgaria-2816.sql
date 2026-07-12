-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source labels available in the downloaded JSON-stat table do not form a verified unique row key; treat rows as source observations rather than keyed records.
SELECT
    "educational_institution_type",
    "school_year_academic_year",
    "ekatte",
    "unit",
    "value"
FROM "statistics-bulgaria-2816"
