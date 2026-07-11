-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The plant inventory does not expose a stable non-null identifier for every row; municipality fields are denormalized into each plant row.
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
    "municipality_code",
    "postcode",
    "address",
    "commissioning_date",
    "hub_height",
    "rotor_diameter",
    "model",
    "gsrn_id",
    "dso",
    "manufacturer"
FROM "open-power-system-data-renewable-power-plants--renewable-power-plants-dk"
