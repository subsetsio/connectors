-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "municipality_ar",
    "households_number",
    "households_percentage_distribution",
    "households_members_number",
    "households_members_percentage_distribution",
    "average_household_size",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-distribution-of-the-number-of-households-and-their-members-by-municipality-census-2015"
