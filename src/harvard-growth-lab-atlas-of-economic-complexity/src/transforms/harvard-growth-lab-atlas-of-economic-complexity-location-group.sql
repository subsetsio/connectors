-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A many-to-many membership table: every country appears in many groups across the ten `group_type` values, and the `world` group contains all of them. Filter `group_type` (and usually a single `group_id`) before aggregating, or every country is counted repeatedly. `group_type` also includes non-geographic, editorial groupings (`rock_song`).
SELECT
    "country_id",
    "country_iso3_code",
    "group_id",
    "group_type",
    "group_name",
    "group_parent_id"
FROM "harvard-growth-lab-atlas-of-economic-complexity-location-group"
