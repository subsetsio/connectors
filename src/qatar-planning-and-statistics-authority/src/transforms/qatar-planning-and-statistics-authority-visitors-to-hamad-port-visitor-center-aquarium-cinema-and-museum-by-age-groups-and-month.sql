-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "visitor_category",
    "fy_lzy_r",
    "number"
FROM "qatar-planning-and-statistics-authority-visitors-to-hamad-port-visitor-center-aquarium-cinema-and-museum-by-age-groups-and-month"
