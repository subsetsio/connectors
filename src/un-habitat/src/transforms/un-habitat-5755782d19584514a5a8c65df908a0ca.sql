-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains several land, street, and intersection indicators; select the relevant metric columns before comparing cities.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "Country" AS country,
    "City" AS city,
    "Pct_Proportion_of_land_Allocate" AS pct_proportion_of_land_allocate,
    "Street_density_Km_per_Km2" AS street_density_km_per_km2,
    "Intersection_density_No_per_Km2" AS intersection_density_no_per_km2,
    "Regions" AS regions,
    "Area_of_Interest" AS area_of_interest,
    "ObjectId" AS objectid
FROM "un-habitat-5755782d19584514a5a8c65df908a0ca"
