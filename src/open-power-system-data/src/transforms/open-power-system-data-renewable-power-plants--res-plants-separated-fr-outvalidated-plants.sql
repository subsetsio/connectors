-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an outvalidated subset of French renewable plant records and does not expose a stable non-null identifier for every row; several geographic labels are denormalized.
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
    "region",
    "region_code",
    "municipality_group",
    "municipality_group_code",
    "departement",
    "departement_code",
    "commissioning_date",
    "connection_date",
    "disconnection_date",
    "number_of_installations",
    "site_name",
    "IRIS_code" AS iris_code,
    "EIC_code" AS eic_code,
    "as_of_year",
    "comment"
FROM "open-power-system-data-renewable-power-plants--res-plants-separated-fr-outvalidated-plants"
