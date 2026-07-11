-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "citizenship",
    "higher_educational_institutions",
    "school_year",
    "country",
    "value"
FROM "geostat-social-20statistics-education-higher-georgian-citizens-studying-abroad-2"
