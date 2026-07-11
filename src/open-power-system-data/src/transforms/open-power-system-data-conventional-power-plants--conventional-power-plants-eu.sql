-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The European conventional plant inventory combines records from many national source lists and does not expose a stable non-null plant identifier for every row.
SELECT
    "name",
    "company",
    "street",
    "postcode",
    "city",
    "country",
    "capacity",
    "energy_source",
    "technology",
    "chp",
    "commissioned",
    "type",
    "lat",
    "lon",
    "eic_code",
    "energy_source_level_1",
    "energy_source_level_2",
    "energy_source_level_3",
    "additional_info",
    "comment",
    "source"
FROM "open-power-system-data-conventional-power-plants--conventional-power-plants-eu"
