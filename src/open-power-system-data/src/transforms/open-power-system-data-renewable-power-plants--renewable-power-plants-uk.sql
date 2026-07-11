-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This national renewable plant inventory is keyed by the UK BEIS source identifier.
SELECT
    "electrical_capacity",
    "energy_source_level_1",
    "energy_source_level_2",
    "energy_source_level_3",
    "technology",
    "data_source",
    "nuts_1_region",
    "nuts_2_region",
    "nuts_3_region",
    "lon",
    "lat",
    "municipality",
    "postcode",
    "address",
    "region",
    "country",
    "commissioning_date",
    "solar_mounting_type",
    "chp",
    "capacity_individual_turbine",
    "number_of_turbines",
    "site_name",
    "uk_beis_id",
    "operator",
    "comment"
FROM "open-power-system-data-renewable-power-plants--renewable-power-plants-uk"
