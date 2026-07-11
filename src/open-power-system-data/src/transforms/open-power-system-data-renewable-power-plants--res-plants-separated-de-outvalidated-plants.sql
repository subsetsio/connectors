-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an outvalidated subset of German renewable plant records and does not expose a stable non-null identifier for every row.
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
    "federal_state",
    "commissioning_date",
    "decommissioning_date",
    "voltage_level",
    "eeg_id",
    "dso",
    "dso_id",
    "tso",
    "comment"
FROM "open-power-system-data-renewable-power-plants--res-plants-separated-de-outvalidated-plants"
