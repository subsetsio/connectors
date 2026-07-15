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
FROM "sg-data-d-dddc19f6c90edd7cff6b57494630ad29"
