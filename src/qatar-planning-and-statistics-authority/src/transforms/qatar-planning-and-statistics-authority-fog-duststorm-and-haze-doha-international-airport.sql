-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "nw_lzhr_ljwy",
    "event_type",
    "value_d"
FROM "qatar-planning-and-statistics-authority-fog-duststorm-and-haze-doha-international-airport"
