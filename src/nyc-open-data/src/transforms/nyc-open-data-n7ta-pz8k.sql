-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "community_school_district",
    "children_aged_410_contributed_per_housing_unit",
    "children_aged_1113_contributed_per_housing_unit",
    "children_aged_1417_contributed_per_housing_unit",
    "data_as_of"
FROM "nyc-open-data-n7ta-pz8k"
