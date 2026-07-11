-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "previous_place_of_residence",
    "sex",
    "usual_place_of_residence",
    "value"
FROM "geostat-population-20census-202014-the-20geographical-20distribution-20of-20the-20population-20and-20internal-20migration-29-internal-migrants-by-previous-and-usual-place-of-residence-and-by-sex"
