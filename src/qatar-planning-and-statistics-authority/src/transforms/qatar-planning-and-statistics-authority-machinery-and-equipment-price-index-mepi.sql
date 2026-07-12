-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code",
    "group_desc_ar",
    "group_desc_en",
    "weight",
    "h1_20",
    "h2_20",
    "h1_21",
    "h2_21",
    "h1_22",
    "h2_22",
    "h1_23",
    "h2_23",
    "h1_24",
    "h2_24"
FROM "qatar-planning-and-statistics-authority-machinery-and-equipment-price-index-mepi"
