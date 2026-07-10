-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_id",
    "release_date",
    "title_en",
    "title_bm",
    "publication_type",
    "publication_type_en",
    "publication_type_bm",
    "frequency",
    "release_series",
    "release_series_date",
    "release_series_en",
    "release_series_bm"
FROM "dosm-arc-dosm"
