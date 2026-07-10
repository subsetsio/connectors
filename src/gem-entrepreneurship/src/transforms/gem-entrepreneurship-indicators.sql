-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table records source variables and labels discovered in public national-level files; a canonical indicator can map to multiple year-specific source variables, especially for APS.
SELECT
    "survey",
    "indicator",
    "variable",
    "label",
    "first_year",
    "last_year"
FROM "gem-entrepreneurship-indicators"
