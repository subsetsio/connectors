-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "Date" AS date,
    "Day" AS day,
    "Subuh" AS subuh,
    "Syuruk" AS syuruk,
    "Zohor" AS zohor,
    "Asar" AS asar,
    "Maghrib" AS maghrib,
    "Isyak" AS isyak
FROM "sg-data-d-e81ea2337599b674c4f645c1af93e0dc"
