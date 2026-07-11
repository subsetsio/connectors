-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source cube has duplicated dimension combinations in the raw profile, so no row key is declared; treat rows as source observation records rather than a uniquely keyed dimensional cube.
SELECT
    "previous_place_of_residence",
    "urban_rural",
    "usual_place_of_residence",
    "value"
FROM "geostat-population-20census-202014-the-20geographical-20distribution-20of-20the-20population-20and-20internal-20migration-29-1-internal-migrants-by-previous-and-usual-place-of-residence"
