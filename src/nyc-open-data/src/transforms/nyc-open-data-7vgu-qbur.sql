-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "section",
    "sectioncode",
    "shape_area",
    "shape_length",
    "multipolygon",
    "objectid"
FROM "nyc-open-data-7vgu-qbur"
