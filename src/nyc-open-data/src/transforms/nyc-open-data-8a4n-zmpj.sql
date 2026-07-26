-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "accession",
    "artwork_title",
    "artist_lastname",
    "artist_firstname",
    "medium",
    "artwork_year",
    "dimension",
    "bldgid",
    "school_name",
    "borough"
FROM "nyc-open-data-8a4n-zmpj"
